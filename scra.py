#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import time

import classes.bridge as bridge
import classes.network as network
import classes.utils as utils
import classes.picklify as picklify

import const


class Scrapy:
    def __init__(self, pages_to_scrape=1):
        if sys.version_info[0] < 3:
            raise Exception('Must be ran using python 3!')

        self.pages_to_scrape = pages_to_scrape

    def _save_ads_debug(self, adverts):
        with open('ads_debug.json', 'w') as f:
            f.write(json.dumps(adverts))

    def run(self):
        current_page = 1
        known_ids = []
        known_adverts = {}

        try:
            known_ids = picklify.unpickle_ids()
            known_adverts = picklify.unpickle_adverts()
            total_previously_adverts = len(known_ids)
            time_start = time.time()
            for p in range(1, self.pages_to_scrape + 1):
                ads = network.get_av_adverts(p)
                self._save_ads_debug(ads)
                for ad in ads:
                    if ad['id'] not in known_ids:  # unique ads only
                        advert, status = bridge.to_auto(ad)
                        known_ids.append(advert.AVID)
                        picklify.pickle_ids(known_ids)
                        picklify.pickle_adverts(known_adverts)
                    else:
                        utils.log('++ Skipping %s - %s, not unique' %
                                  (ad['title'], ad['id']), const.LOG_LEVEL_HIGH)
            utils.log('*' * 80, const.LOG_LEVEL_HIGH)
            res = 'Scraped %d new adverts in %d seconds' \
                % ((len(known_ids) - total_previously_adverts), (time.time() - time_start))
            print('-- %s --' % res, const.LOG_LEVEL_HIGH)
            utils.speak(res)
            utils.log('*' * 80, const.LOG_LEVEL_HIGH)
        except Exception as e:
            utils.speak('I\'m sorry but I failed!')
            raise(e)


Scrapy().run()
