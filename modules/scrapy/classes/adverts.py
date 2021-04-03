import json

class BaseAdvert:
  AVID = None
  ID = None
  ParentID = 6
  CanReceiveMessages = False
  Images = []
  Title = None #min 8 chars
  Content = None
  ParentCategoryID = None
  CategoryID = None
  Price = None
  Negotiable = False
  SiteCurrencyID = 1
  Status = None
  ParentCityID = None
  CityID = None
  Phone = None

  # to string override for printing
  def __str__(self):
    lines = [self.__class__.__name__ + ':']
    for key, val in vars(self).items():
        lines += '{}: {}'.format(key, val).split('\n')
    return '\n  '.join(lines)

  def to_json(self):
    return json.dumps(self.__dict__)

class AutoAdvert(BaseAdvert):
  BrandID = None
  BrandModelID = None
  FabricationYear = None
  KmNumber = None
  VIN = None
  FuelID = None
  ColorID = None
  MetallicColor = False
  CarOptions = None
  CubicCapacity = None
  HorsePower = None
  GearboxTypeID = None
  TransmissionTypeID = None
  DoorsNumber = None
  PollutionNormID = None
  ParticleFilter = False
  FuelConsumption = None
  Matriculated = None
  FirstOwner = False
  NoAccidents = False
  ServiceBook = False
  Tuning = False
  CountryID = None