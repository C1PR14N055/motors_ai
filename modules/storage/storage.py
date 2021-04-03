# -*- coding: utf-8 -*-

class Shelf():
    def _load_data(self):
        self.known_ids = picklify.unpickle_ids()
        self.known_adverts = picklify.unpickle_adverts()
        self.total_previously_adverts = len(known_ids)

    def __init__(self):
        self._load_data()
        print("Loading data...")
        print(self.known_ids[:10])
