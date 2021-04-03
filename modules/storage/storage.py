# -*- coding: utf-8 -*-
import pickle


class Shelf():
    def __init__(self):
        self._load_data()
        print("Loading data...")
        print(self.known_ids)

    def _load_data(self):
        self.known_ids = self.unpickle_ids()
        self.known_adverts = self.unpickle_adverts()
        # self.total_previously_adverts = len(self.known_ids)

    def pickle_ids(self, ids):
        with open('pickle_jar/ids.pkl', 'wb') as f:
            pickle.dump(ids, f)
            f.close()

    def unpickle_ids(self):
        try:
            with open('pickle_jar/ids.pkl', 'rb') as f:
                ids = pickle.load(f)
                return ids
        except OSError:
            raise OSError

    def pickle_adverts(self, adverts):
        with open('pickle_jar/adverts.pkl', 'wb') as f:
            pickle.dump(adverts, f)
            f.close()

    def unpickle_adverts(self):
        try:
            with open('pickle_jar/adverts.pkl', 'rb') as f:
                adverts = pickle.load(f)
            return adverts
        except OSError:
            return {'success': [], 'failed': []}
