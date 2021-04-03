# -*- coding: utf-8 -*-
import pickle

class Shelf():
    def _load_data(self):
        self.known_ids = self.unpickle_ids()
        self.known_adverts = self.unpickle_adverts()
        self.total_previously_adverts = len(self.known_ids)

    def __init__(self):
        self._load_data()
        print("Loading data...")
        print(self.known_ids[:10])

    def pickle_ids(ids):
        with open('pickles/ids.pkl', 'wb') as f:
            pickle.dump(ids, f)
            f.close()


    def unpickle_ids():
        try:
            with open('pickles/ids.pkl', 'rb') as f:
                ids = pickle.load(f)
                return ids
        except:
            return []


    def pickle_adverts(adverts):
        with open('pickles/adverts.pkl', 'wb') as f:
            pickle.dump(adverts, f)
            f.close()


    def unpickle_adverts():
        try:
            with open('pickles/adverts.pkl', 'rb') as f:
                adverts = pickle.load(f)
            return adverts
        except:
            return {'success': [], 'failed': []}