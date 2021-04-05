# -*- coding: utf-8 -*-
from modules.utils.utils import Tools
from modules.storage import Shelf
from modules.scrapy import Scrapy, scra
from modules.jarvis import Jarvis
import sys

if sys.version_info[0] < 3:
    raise Exception('Must be ran using python 3!')

# TODO: args parse

EXEC_SCRAPY = not True
PAGES_TO_SCRAPE = 1
EXEC_JARVIS = True
TEST_CAR = [
    14,     # brand id, bmw
    177,    # model id, series 3
    2010,   # fab year
    13,     # CityID,  13 = Arad
    6,      # PollutionNormID, 6 = Euro 5
    9,      # CountryID, 9 = Germany
    3,      # Status, 3 = used
    True,   # Matriculated
    True,   # ServiceBook
    True,   # ParticleFilter
    True,   # MetallicColor
    False,  # FirstOwner
    False,  # NoAccidents
    False,  # Tuning
    False,  # Negotiable
    2000,   # CubicCapacity
    240000,  # KmNumber
    184,    # HorsePoser
    4       # DoorsNumber
]

if EXEC_SCRAPY:
    scrapy = Scrapy(PAGES_TO_SCRAPE)
    scrapy.run()
if EXEC_JARVIS:
    jarvis = Jarvis()
    jarvis.build_model()
    predicted = jarvis.predict(TEST_CAR)
    Tools.log('** Predicted price for **')
    Tools.log(TEST_CAR)
    Tools.log('** ==> {} EUR <== **'.format(predicted))
    # jarvis.plot_years()
    # jarvis.plot_hp()
    # jarvis.build_model()
