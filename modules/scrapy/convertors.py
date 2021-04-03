import json

import config as CFG
from .models import AutoAdvert
from .http import FakeBrowser
from ..utils import Tools


class Transformer:
    def to_base(data):
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

    def to_auto(data):
        # static stuff
        advert, status = to_base(data)
        if not status:
            return advert, False
        advert.ParentCategoryID = 1
        # guesses
        advert.CategoryID = guess_category(get_data_param('Caroserie', data))
        advert.ParentCityID, advert.CityID = guess_cities(data['city_name'])
        advert.BrandID, advert.BrandModelID = guess_brand_model(get_data_param(
            'Marca', data), get_data_param('Model', data), get_data_param('Versiune', data))
        advert.ColorID = guess_color(get_data_param('Culoare', data))
        advert.FuelID = guess_fuel(get_data_param('Combustibil', data))
        advert.GearboxTypeID = guess_gearbox(
            get_data_param('Cutie de viteze', data))
        advert.TransmissionTypeID = guess_transmission(
            get_data_param('Transmisie', data))
        advert.PollutionNormID = guess_pollution(
            get_data_param('Norma de poluare', data))
        advert.CountryID = guess_country(
            get_data_param('Tara de origine', data))
        advert.Status = guess_status(get_data_param('Stare', data))
        # boolean values
        advert.Matriculated = guess_boolean('Inmatriculat', data)
        advert.ServiceBook = guess_boolean('Carte de service', data)
        advert.ParticleFilter = guess_boolean('Filtru de particule', data)
        advert.MetallicColor = guess_boolean('Vopsea metalizata', data)
        advert.FirstOwner = guess_boolean('Primul proprietar', data)
        advert.NoAccidents = guess_boolean('Fara accident in istoric', data)
        advert.Tuning = guess_boolean('Tuning', data)
        advert.Negotiable = guess_negotiable(data)
        # string values
        advert.VIN = get_data_param('VIN', data)
        # numeric values
        advert.CubicCapacity = guess_number('Capacitate cilindrica', data)
        advert.KmNumber = guess_number('Km', data)
        advert.HorsePower = guess_number('Putere', data)
        advert.DoorsNumber = guess_number('Numar de portiere', data)
        advert.FabricationYear = guess_number('Anul fabricatiei', data)
        advert.Price = Tools.strip_number(data['list_label'])
        advert.PollutionNumber = guess_number('Emisii CO2', data)
        # options
        advert.CarOptions = guess_options(data)
        # ajax phone nr
        try:
            advert.Phone = FakeBrowser.get_av_phone(data)
        except Exception:
            return advert, False

        Tools.log(advert, const.LOG_LEVEL_LOW)
        return advert, True

    def to_moto(data):
        advert = to_base(data)
        advert.ParentCategoryID = 10
        return advert

    def get_data_param(name, data):
        for p in data['params']:
            if p[0] == name:
                return p[1]
        else:
            return None

    def guess_category(categoryName):
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
        category, bid = guess('categories', categoryName, 1)
        if bid < 0.7:
            category = get_api_param('categories', 9)  # default to 'Altele'

        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, tmpCategoryName, category['Title']),
                  )
        return category['ID']

    def guess_cities(cityName):
        city, bid = guess('cities', cityName, True)
        if bid < 0.7:  # default to 'Bucuresti'
            city = get_api_param('cities', 360)
        parentCity = get_api_param('cities', city['Parent'])
        Tools.log('%d%% sure %s = %s, %s' %
                  (bid * 100, cityName, parentCity['Title'], city['Title'])
                  )
        return (parentCity['ID'], city['ID'])

    def guess_brand_model(brandName, modelName, versionName):
        brand, bbid = guess('brands', brandName)
        if bbid < 0.7:
            brand = get_api_param('brands', 114)  # default to 'Altele'
            brandModel = get_api_param('models', 2145)  # default to 'Altele'
            return (brand['ID'], brandModel['ID'])

        model, mbid = guess('models', modelName)
        version, vbid = guess('models', versionName)

        brandModel = model if mbid > vbid else version
        bmbid = mbid if mbid > vbid else vbid

        if bmbid < 0.7:  # default to 'Altele' from this brand
            with open('data/models.json', 'r') as f:
                models = json.load(f)
            for m in models:
                if m['Parent'] == brand['ID'] and m['Title'] == 'Altele':
                    brandModel = m
                    break

        Tools.log('%d%% sure %s %s %s = %s, %s' % (
            bmbid * 100,
            brandName,
            modelName,
            versionName or '-',
            brand['Title'],
            brandModel['Title'])
        )
        return (brand['ID'], brandModel['ID'])

    def guess_color(colorName):
        color, bid = guess('colors', colorName)
        if bid < 0.7:
            color = get_api_param('colors', 12)

        Tools.log('%d%% sure %s = %s' % (bid * 100, colorName, color['Title']))
        return color['ID']

    def guess_fuel(fuelName):
        fuel, bid = guess('fuels', fuelName)
        if bid < 0.7:  # default to 'Manuala'
            fuel = get_api_param('fuels', 1)
        Tools.log('%d%% sure %s = %s' % (bid * 100, fuelName, fuel['Title']))
        return fuel['ID']

    def guess_gearbox(gearboxName):
        gear, bid = guess('gearboxes', gearboxName)
        if bid < 0.7:  # default to 'Manuala'
            gear = get_api_param('gearboxes', 1)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, gearboxName, gear['Title']))
        return gear['ID']

    def guess_transmission(transmissionName):
        transmission, bid = guess('transmissions', transmissionName)
        if bid < 0.7:
            transmission = get_api_param('transmissions', 1)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, transmissionName, transmission['Title']))
        return transmission['ID']

    def guess_pollution(pollutionName):
        pollution, bid = guess('pollutions', pollutionName)
        if (bid < 0.7):
            pollution = get_api_param('pollutions', 5)  # default to 'Euro 4'
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, pollutionName, pollution['Title']))
        return pollution['ID']

    def guess_country(countryName):
        country, bid = guess('countries', countryName)
        if (bid < 0.7):
            country = get_api_param('countries', 1)  # default to 'Romania'
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, countryName, country['Title']))
        return country['ID']

    def guess_status(statusName):
        status, bid = guess('statuses', statusName)
        if bid < 0.7:
            status = get_api_param('statuses', 3)
        Tools.log('%d%% sure %s = %s' %
                  (bid * 100, statusName, status['Title']))
        return status['ID']

    def guess_boolean(booleanName, data):
        Tools.log(
            '100%% sure %s = %s' %
            (
                booleanName,
                True if get_data_param(booleanName, data) is not None
                and get_data_param(booleanName, data) else False
            )
        )
        return True if get_data_param(booleanName, data) is not None \
            and get_data_param(booleanName, data) else False

    def guess_number(numberName, data):
        if get_data_param(numberName, data) is not None:
            return Tools.strip_number(get_data_param(numberName, data))
        else:
            return None

    def guess_negotiable(data):
        return 'Negociabil' in data['list_label_small']

    def guess_options(data):
        options = []
        if 'features' in data:
            for f in data['features']:
                option, bid = guess('options', f)
                if bid > 0.7 and option['ID'] not in options:
                    options.append(option['ID'])
        return options

    def guess(param, searchTerm, parent=False):
        if param is None or searchTerm is None:
            return None, -1

        with open('data/{0}.json'.format(param), 'r') as f:
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

        Tools.log('%d%% sure \'%s\' === \'%s\'' %
                  (bid * 100, searchTerm, found['Title']))
        return (found, bid)

    def get_api_param(param, id):
        with open(('data/{0}.json'.format(param)), 'r') as f:
            data = json.load(f)

        for d in data:
            if (d['ID'] == id):
                return d
        else:
            return None
