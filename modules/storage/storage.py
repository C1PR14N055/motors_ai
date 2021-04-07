# -*- coding: utf-8 -*-
import pickle
from ..utils import Tools
from datetime import datetime, timezone
import gzip
import json
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls]


class Shelf(metaclass=Singleton):
    def __init__(self):
        Tools.log('++ Loading data...', Tools.LOG_LEVEL_HIGH)
        self._load_data()
        Tools.log(
            '** Total known adverts: %d' %
            self.total_known_adverts, Tools.LOG_LEVEL_HIGH
        )

    def _load_data(self):
        self.known_ids = self.deserialize_ids()
        self.adverts = self.deserialize_adverts()
        self.total_known_adverts = len(self.known_ids)

    def _filename_now(self, filename):
        return '{}_{}.gz'.format(
            datetime.now(timezone.utc).strftime('%d-%m-%Y@%H:%M:%S'),
            filename,
        )

    def save_ads_debug(self, adverts):
        try:
            os.mkdir('database/autovit/')
        except FileExistsError:
            pass
        with open('database/autovit/last_adverts_debug.json', 'w') as f:
            f.write(json.dumps(adverts, indent=4))
        with open('database/autovit/last_advert_debug.json', 'w') as f:
            f.write(json.dumps(adverts[-1:], indent=4))

    def serialize_ids(self, ids):
        try:
            os.mkdir('database/autovit/')
        except FileExistsError:
            pass
        with gzip.open('database/autovit/scraped_ids.gz', 'w') as fout:
            fout.write(json.dumps(ids).encode('utf-8'))

    def deserialize_ids(self):
        try:
            with gzip.open('database/autovit/scraped_ids.gz', 'r') as fin:
                ids = json.loads(fin.read().decode('utf-8'))
                return ids
        except FileNotFoundError:
            return []

    def serialize_adverts(self, adverts):
        try:
            os.mkdir('database/autovit/adverts/')
        except FileExistsError:
            pass

        filename = self._filename_now('{}_adverts'.format(len(adverts)))
        with gzip.open(os.path.join('database/autovit/adverts', filename).format(), 'w') as fout:
            fout.write(json.dumps(adverts).encode('utf-8'))

    def deserialize_adverts(self):
        adverts = []
        for root, dirs, files in os.walk('database/autovit/adverts/'):
            for name in files:
                file = os.path.join(root, name)
                Tools.log('++ Loading: {}'.format(name))
                with gzip.open(file, 'r') as fin:
                    adverts.extend(json.loads(fin.read().decode('utf-8')))
            return adverts
        else:
            return []
