# -*- coding: utf-8 -*-
from modules.utils.utils import Tools
from modules.storage import Shelf
from modules.scrapy import Scrapy, scra
from modules.jarvis import Jarvis
import sys

if sys.version_info[0] < 3:
    raise Exception('Must be ran using python 3!')

# TODO: args parse

EXEC_SCRAPY = True
PAGES_TO_SCRAPE = 100
EXEC_JARVIS = not True
'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TO TEST A CAR GET BrandID FROM `data/brands.json`
AND ModelID FROM `data/models.json'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''
TEST_CAR = [
    # 14,     # BrandID, bmw
    # 177,    # ModelID, series 3
    # 2004,   # fab year
    # 13,     # CityID, 13 = Arad (categorical data?)
    # 5,      # PollutionNormID, 6 = Euro 5
    # 9,      # CountryID, 9 = Germany
    # 3,      # Status, 3 = used
    # True,   # Matriculated
    # True,   # ServiceBook
    # True,   # ParticleFilter
    # True,   # MetallicColor
    # False,  # FirstOwner
    # True,  # NoAccidents
    # False,  # Tuning
    # True,  # Negotiable
    # 1995,   # CubicCapacity
    240000,  # KmNumber
    # 184,    # HorsePoser
    # 4       # DoorsNumber (TODO: merge 2/3 && 4/5)
]

if EXEC_SCRAPY:
    scrapy = Scrapy(PAGES_TO_SCRAPE)
    scrapy.run()
if EXEC_JARVIS:
    jarvis = Jarvis()

    jarvis.build_model()
    prediction = jarvis.predict(TEST_CAR)
    Tools.log('** Predicted price for ==> {} EUR'.format(prediction))
