# -*- coding: utf-8 -*-
from core import Config
from ..storage import Shelf
from ..utils import Tools
from .http import FakeBrowser
from .convertors import Transformer

import json
import time

# TODO: refactor to not use ids.pkl
# TODO: refactor to save crawl with time info


class Scrapy:
    shelf = Shelf()
    # transformer = Transformer()

    def __init__(self, pages_to_scrape=1):
        self.pages_to_scrape = pages_to_scrape

    def run(self):
        try:
            total_previously_adverts = len(self.shelf.known_ids)
            time_start = time.time()
            new_adverts = []
            for p in range(1, self.pages_to_scrape + 1):
                # adverts in one page
                adverts = FakeBrowser.steal_adverts(p)
                # filter adverts for already seen ones
                adverts = [adv for adv in adverts if adv['id']
                           not in self.shelf.known_ids]
                Tools.log('++ Got %d new adverts' % len(adverts))
                # append filtered to new_adverts
                new_adverts.extend(adverts)

            # save last known ids
            self.shelf.known_ids.extend(
                [advert['id'] for advert in new_adverts]
            )
            self.shelf.serialize_ids(self.shelf.known_ids)

            # save last ads for debug
            self.shelf.save_ads_debug(new_adverts)

            # save lastest scraped ads
            self.shelf.serialize_adverts(new_adverts)

            res = 'Scraped a total of %d new adverts in %d seconds' \
                % (
                    (len(self.shelf.known_ids) - total_previously_adverts),
                    (time.time() - time_start)
                )
            Tools.log('++ %s ++' % res, Tools.LOG_LEVEL_HIGH)
            Tools.speak(res)
        except Exception as e:
            Tools.speak('I\'m sorry but I failed!')
            raise(e)
