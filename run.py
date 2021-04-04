# -*- coding: utf-8 -*-
from modules.storage import Shelf
from modules.scrapy import Scrapy
from modules.jarvis import Jarvis
# from core import MotorsAI
import sys

if sys.version_info[0] < 3:
    raise Exception('Must be ran using python 3!')

# TODO: args parse
pages_to_scrape = 1

# scrapy = Scrapy(pages_to_scrape).run()

jarvis = Jarvis()
# MotorsAI.run()
