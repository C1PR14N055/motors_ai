# -*- coding: utf-8 -*-
import config as GLOBAL_CONFIG
from modules.storage import Shelf
from modules.scrapy import Scrapy

from core import MotorsAI
# import sys
# sys.path.insert(1, "/path/to/application/app/folder")

shelf = Shelf()
Scrapy.run()
MotorsAI.run()
