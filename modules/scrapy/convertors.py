import json

from core import Config
from ..utils import Tools
from .models import AutoAdvert
from .http import FakeBrowser


class Transformer:
    def to_base(self, data):
        advert = AutoAdvert()
        advert.ParentID = 6
        advert.AVID = data['id']  # autovit id reference
        advert.ID = None  # asistcar id future ref
        advert.SiteCurrencyID = 1  # default to EUR
        try:
            advert.Title = data['title']
            advert.Content = data['description'] or 'Fara descriere'
            advert.Images = [p['3'] for p in data['photos'] if '3' in p]
            return advert, True
        except Exception:
            return advert, False

    def to_auto(self, data):
        # static stuff
        advert, status = self.to_base(data)
        if not status:
            return advert, False
        advert.ParentCategoryID = 1
        # guesses
        advert.CategoryID = self._guess_category(
            self._get_data_param('Caroserie', data))
        advert.ParentCityID, advert.CityID = self._guess_cities(
            data['city_name'])
        advert.BrandID, advert.BrandModelID = self._guess_brand_model(
            self._get_data_param
            ('Marca', data),
            self._get_data_param('Model', data),
            self._get_data_param('Versiune', data)
        )
        advert.ColorID = self._guess_color(
            self._get_data_param('Culoare', data))
        advert.FuelID = self._guess_fuel(
            self._get_data_param('Combustibil', data))
        advert.GearboxTypeID = self._guess_gearbox(
            self._get_data_param('Cutie de viteze', data))
        advert.TransmissionTypeID = self._guess_transmission(
            self._get_data_param('Transmisie', data))
        advert.PollutionNormID = self._guess_pollution(
            self._get_data_param('Norma de poluare', data))
        advert.CountryID = self._guess_country(
            self._get_data_param('Tara de origine', data))
        advert.Status = self._guess_status(self._get_data_param('Stare', data))
        # boolean values
        advert.Matriculated = self._guess_boolean('Inmatriculat', data)
        advert.ServiceBook = self._guess_boolean('Carte de service', data)
        advert.ParticleFilter = self._guess_boolean(
            'Filtru de particule', data)
        advert.MetallicColor = self._guess_boolean('Vopsea metalizata', data)
        advert.FirstOwner = self._guess_boolean('Primul proprietar', data)
        advert.NoAccidents = self._guess_boolean(
            'Fara accident in istoric', data)
        advert.Tuning = self._guess_boolean('Tuning', data)
        advert.Negotiable = self._guess_negotiable(data)
        # string values
        advert.VIN = self._get_data_param('VIN', data)
        # numeric values
        advert.CubicCapacity = self._guess_number(
            'Capacitate cilindrica', data)
        advert.KmNumber = self._guess_number('Km', data)
        advert.HorsePower = self._guess_number('Putere', data)
        advert.DoorsNumber = self._guess_number('Numar de portiere', data)
        advert.FabricationYear = self._guess_number('Anul fabricatiei', data)
        advert.Price = Tools.strip_number(data['list_label'])
        advert.PollutionNumber = self._guess_number('Emisii CO2', data)
        # options
        advert.CarOptions = self._guess_options(data)
        # ajax phone nr
        try:
            advert.Phone = FakeBrowser.get_av_phone(data)
        except Exception:
            return advert, False

        Tools.log(advert, Config.LOG_LEVEL_LOW)
        return advert, True

    def to_moto(self, data):
        advert = self.to_base(data)
        advert.ParentCategoryID = 10
        return advert

    def _get_data_param(self, name, data):
        for p in data['params']:
            if p[0] == name:
                return p[1]
        else:
            return None

    def _guess_category(self, categoryName):
        tmpCategoryName = categoryName
        if Tools.similar(tmpCategoryName, 'Cabrio') > 0.9:
            categoryName = 'Cabriolet/Roadster'
        if Tools.similar(tmpCategoryName, 'Monovolum') > 0.9:
            categoryName = 'Microbuz/Furgoneta'
        if Tools.similar(tmpCategoryName, 'Sedan') > 0.9:
            categoryName = 'Berlina'
        if Tools.similar(tmpCategoryName, 'Coupe') > 0.9:
            categoryName = 'Coupe/Sport'
        if Tools.similar(tmpCategoryName, 'Masina mica') > 0.9 \
                or Tools.similar(tmpCategoryName, 'Masina de oras') > 0.9 \
                or Tools.similar(tmpCategoryName, 'Combi') \
                or Tools.similar(tmpCategoryName, 'Compacta') > 0.9:
            categoryName = 'Break'
        category, bid = self._guess('categories', categoryName, 1)
        if bid < 0.7:
            category = self._get_api_param(
                'categories', 9
            )  # default to 'Altele'

        Tools.log(
            '%d%% sure %s = %s' %
            (bid * 100, tmpCategoryName, category['Title']),
        )
        return category['ID']

    def _guess_cities(self, cityName):
        city, bid = self._guess('cities', cityName, True)
        if bid < 0.7:  # default to 'Bucuresti'
            city = self._get_api_param('cities', 360)
        parentCity = self._get_api_param('cities', city['Parent'])
        Tools.log('%d%% sure %s = %s, %s' %
                  (bid * 100, cityName, parentCity['Title'], city['Title'])
                  )
        return (parentCity['ID'], city['ID'])

    def _guess_brand_model(self, brandName, modelName, versionName):
        brand, bbid = self._guess('brands', brandName)
        if bbid < 0.7:
            brand = self._get_api_param('brands', 114)  # default to 'Altele'
            brandModel = self._get_api_param(
                'models', 2145)  # default to 'Altele'
            return (brand['ID'], brandModel['ID'])

        model, mbid = self._guess('models', modelName)
        version, vbid = self._guess('models', versionName)

        brandModel = model if mbid > vbid else version
        bmbid = mbid if mbid > vbid else vbid

        if bmbid < 0.7:  # default to 'Altele' from this brand
            with open('./modules/scrapy/data/models.json', 'r') as f:
                models = json.load(f)
            for m in models:
                if m['Parent'] == brand['ID'] and m['Title'] == 'Altele':
                    brandModel = m
                    break
        Tools.log(
            '%d%% sure %s %s %s = %s, %s'
            % (
                bmbid * 100,
                brandName,
                modelName,
                versionName or '-',
                brand['Title'],
                brandModel['Title']
            )
        )
        return (brand['ID'], brandModel['ID'])

    def _guess_color(self, colorName):
        color, bid = self._guess('colors', colorName)
        if bid < 0.7:
            color = self._get_api_param('colors', 12)

        Tools.log('%d%% sure %s = %s' % (bid * 100, colorName, color['Title']))
        return color['ID']

    def _guess_fuel(self, fuelName):
        fuel, bid = self._guess('fuels', fuelName)
        if bid < 0.7:  # default to 'Manuala'
            fuel = self._get_api_param('fuels', 1)
        Tools.log('%d%% sure %s = %s' % (bid * 100, fuelName, fuel['Title']))
        return fuel['ID']

    def _guess_gearbox(self, gearboxName):
        gear, bid = self._guess('gearboxes', gearboxName)
        if bid < 0.7:  # default to 'Manuala'
            gear = self._get_api_param('gearboxes', 1)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, gearboxName, gear['Title']))
        return gear['ID']

    def _guess_transmission(self, transmissionName):
        transmission, bid = self._guess('transmissions', transmissionName)
        if bid < 0.7:
            transmission = self._get_api_param('transmissions', 1)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, transmissionName, transmission['Title']))
        return transmission['ID']

    def _guess_pollution(self, pollutionName):
        pollution, bid = self._guess('pollutions', pollutionName)
        if (bid < 0.7):
            pollution = self._get_api_param(
                'pollutions', 5)  # default to 'Euro 4'
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, pollutionName, pollution['Title']))
        return pollution['ID']

    def _guess_country(self, countryName):
        country, bid = self._guess('countries', countryName)
        if (bid < 0.7):
            country = self._get_api_param(
                'countries', 1)  # default to 'Romania'
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, countryName, country['Title']))
        return country['ID']

    def _guess_status(self, statusName):
        status, bid = self._guess('statuses', statusName)
        if bid < 0.7:
            status = self._get_api_param('statuses', 3)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, statusName, status['Title']))
        return status['ID']

    def _guess_boolean(self, booleanName, data):
        Tools.log(
            '100%% sure %s = %s' %
            (
                booleanName,
                True if self._get_data_param(booleanName, data) is not None
                and self._get_data_param(booleanName, data) else False
            )
        )
        return True if self._get_data_param(booleanName, data) is not None \
            and self._get_data_param(booleanName, data) else False

    def _guess_number(self, numberName, data):
        if self._get_data_param(numberName, data) is not None:
            return Tools.strip_number(self._get_data_param(numberName, data))
        else:
            return None

    def _guess_negotiable(self, data):
        return 'Negociabil' in data['list_label_small']

    def _guess_options(self, data):
        options = []
        if 'features' in data:
            for f in data['features']:
                option, bid = self._guess('options', f)
                if bid > 0.7 and option['ID'] not in options:
                    options.append(option['ID'])
        return options

    def _guess(self, param, searchTerm, parent=False):
        if param is None or searchTerm is None:
            return None, -1
        with open('./modules/scrapy/data/{0}.json'.format(param), 'r') as f:
            params = json.load(f)
        bid = 0
        found = None
        for p in params:
            if type(parent) == bool and parent:
                if 'Parent' in p \
                        and Tools.similar(p['Title'], searchTerm) > bid:
                    found = p
                    bid = Tools.similar(p['Title'], searchTerm)
            elif type(parent) == int:
                if 'Parent' in p \
                    and p['Parent'] == parent \
                        and Tools.similar(p['Title'], searchTerm) > bid:
                    found = p
                    bid = Tools.similar(p['Title'], searchTerm)
            else:
                if Tools.similar(p['Title'], searchTerm) > bid:
                    found = p
                    bid = Tools.similar(p['Title'], searchTerm)

        if found:
            Tools.log(
                '%d%% sure \'%s\' === \'%s\''
                % (bid * 100, searchTerm, found['Title'])
            )
        return (found, bid)

    def _get_api_param(self, param, id):
        with open(('./modules/scrapy/data/{0}.json'.format(param)), 'r') as f:
            data = json.load(f)
        for d in data:
            if (d['ID'] == id):
                return d
        else:
            return None
