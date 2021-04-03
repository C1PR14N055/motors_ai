import pickle


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
