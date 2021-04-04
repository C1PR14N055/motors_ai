# -*- coding: utf-8 -*-
from modules.utils.utils import Tools
from modules.storage import Shelf
from modules.scrapy import Scrapy, scra
from modules.jarvis import Jarvis
import sys

if sys.version_info[0] < 3:
    raise Exception('Must be ran using python 3!')

# TODO: args parse

SCRAPY = True
JARVIS = True

if SCRAPY:
    scrapy = Scrapy(1)
    scrapy.run()
if JARVIS:
    jarvis = Jarvis()
    jarvis.show_plots()
    # jarvis.test()
    # Tools.log('asdfsaf', Tools.LOG_LEVEL_SPEAK)
    # Tools.speak(' hope u slept well')
