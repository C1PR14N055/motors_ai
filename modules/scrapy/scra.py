# -*- coding: utf-8 -*-
from core import Config
from ..storage import Shelf
from ..utils import Tools
from .http import FakeBrowser
from .convertors import Transformer

import json
import sys
import time

# TODO: refactor to not use ids.pkl
# TODO: refactor to save crawl with time info


class Scrapy:
    shelf = Shelf()
    transformer = Transformer()

    def __init__(self, pages_to_scrape=1):
        self.pages_to_scrape = pages_to_scrape

    def _save_ads_debug(self, adverts):
        with open('ads_debug.json', 'w') as f:
            f.write(json.dumps(adverts))

    def run(self):
        try:
            total_previously_adverts = len(self.shelf.known_ids)
            time_start = time.time()
            for p in range(1, self.pages_to_scrape + 1):
                ads = FakeBrowser.steal_adverts(p)
                self._save_ads_debug(ads)
                for ad in ads:
                    if ad['id'] not in self.shelf.known_ids:  # unique ads only
                        advert, status = self.transformer.to_auto(ad)
                        self.shelf.known_ids.append(advert.AVID)
                        self.shelf.pickle_ids(self.shelf.known_ids)
                        if status:
                            self.shelf.adverts_ok.append(advert)
                        else:
                            self.shelf.adverts_err.append(advert)
                        self.shelf.pickle_adverts(
                            self.shelf.adverts_ok,
                            self.shelf.adverts_err
                        )
                    else:
                        Tools.log(
                            '++ Skipping %s - %s, not unique'
                            % (ad['title'], ad['id']), Tools.LOG_LEVEL_HIGH
                        )
            Tools.log('*' * 80, Tools.LOG_LEVEL_HIGH)
            res = 'Scraped %d new adverts in %d seconds' \
                % (
                    (len(self.shelf.known_ids) - total_previously_adverts),
                    (time.time() - time_start)
                )
            Tools.log('-- %s --' % res, Tools.LOG_LEVEL_HIGH)
            Tools.speak(res)
            Tools.log('*' * 80, Tools.LOG_LEVEL_HIGH)
        except Exception as e:
            Tools.speak('I\'m sorry but I failed!')
            raise(e)
