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

if EXEC_SCRAPY:
    scrapy = Scrapy(PAGES_TO_SCRAPE)
    scrapy.run()
if EXEC_JARVIS:
    jarvis = Jarvis()
    jarvis.plot_years()
    jarvis.plot_hp()
    jarvis.stats()
