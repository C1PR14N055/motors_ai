# -*- coding: utf-8 -*-
from modules.storage import Shelf
from modules.scrapy import Scrapy
# from core import MotorsAI

# TODO: args parse
pages_to_scrape = 2

Scrapy(pages_to_scrape).run()
# MotorsAI.run()
