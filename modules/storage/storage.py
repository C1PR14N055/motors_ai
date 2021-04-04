# -*- coding: utf-8 -*-
import pickle
from core import Config
from ..utils import Tools


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
        self._load_data()
        Tools.log('** Loading data... **', Config.LOG_LEVEL_HIGH)
        Tools.log(
            '** Total known adverts: %d **' %
            self.total_known_adverts, Config.LOG_LEVEL_HIGH
        )

    def _load_data(self):
        self.known_ids = self.unpickle_ids()
        self.adverts_ok, self.adverts_err = self.unpickle_adverts()
        self.total_known_adverts = len(self.known_ids)

    def pickle_ids(self, ids):
        with open('pickle_jar/ids.pkl', 'wb') as f:
            pickle.dump(ids, f)
            f.close()

    def unpickle_ids(self):
        try:
            with open('pickle_jar/ids.pkl', 'rb') as f:
                ids = pickle.load(f)
                return ids
        except FileNotFoundError:
            return []

    def pickle_adverts(self, adverts_ok, adverts_err):
        with open('pickle_jar/adverts_ok.pkl', 'wb') as f:
            pickle.dump(adverts_ok, f)
            f.close()
        with open('pickle_jar/adverts_err.pkl', 'wb') as f:
            pickle.dump(adverts_err, f)
            f.close()

    def unpickle_adverts(self):
        try:
            with open('pickle_jar/adverts_ok.pkl', 'rb') as f:
                adverts_ok = pickle.load(f)
            with open('pickle_jar/adverts_err.pkl', 'rb') as f:
                adverts_err = pickle.load(f)
            return adverts_ok, adverts_err
        except FileNotFoundError:
            return [], []
