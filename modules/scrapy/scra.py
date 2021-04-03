# -*- coding: utf-8 -*-
from core import Config
from ..storage import Shelf
from ..utils import Tools
from .http import FakeBrowser
from .convertors import Transformer

import json
import sys
import time


class Scrapy:
    shelf = Shelf()
    transformer = Transformer()

    def __init__(self, pages_to_scrape=1):
        if sys.version_info[0] < 3:
            raise Exception('Must be ran using python 3!')

        self.pages_to_scrape = pages_to_scrape

    def _save_ads_debug(self, adverts):
        with open('ads_debug.json', 'w') as f:
            f.write(json.dumps(adverts))

    def run(self):
        known_ids = []
        known_adverts = {}

        try:
            known_ids = self.shelf.unpickle_ids()
            known_adverts = self.shelf.unpickle_adverts()
            total_previously_adverts = len(known_ids)
            time_start = time.time()
            for p in range(1, self.pages_to_scrape + 1):
                ads = FakeBrowser.steal_adverts(p)
                self._save_ads_debug(ads)
                for ad in ads:
                    if ad['id'] not in known_ids:  # unique ads only
                        advert, status = self.transformer.to_auto(ad)
                        known_ids.append(advert.AVID)
                        self.shelf.pickle_ids(known_ids)
                        self.shelf.pickle_adverts(known_adverts)
                    else:
                        Tools.log(
                            '++ Skipping %s - %s, not unique'
                            % (ad['title'], ad['id']), Config.LOG_LEVEL_HIGH
                        )
            Tools.log('*' * 80, Config.LOG_LEVEL_HIGH)
            res = 'Scraped %d new adverts in %d seconds' \
                % (
                    (len(known_ids) - total_previously_adverts),
                    (time.time() - time_start)
                )
            Tools.log('-- %s --' % res, Config.LOG_LEVEL_HIGH)
            Tools.speak(res)
            Tools.log('*' * 80, Config.LOG_LEVEL_HIGH)
        except Exception as e:
            Tools.speak('I\'m sorry but I failed!')
            raise(e)
