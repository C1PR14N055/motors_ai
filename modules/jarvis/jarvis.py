from ..utils import Tools
from ..storage import Shelf

import pandas as pd
import numpy as np


class Jarvis():
    def __init__(self):
        self.shelf = Shelf()
        adverts_ok, adverts_err = self.shelf.unpickle_adverts()
        print(adverts_ok[0])
        print(adverts_err)
        # df = pd.DataFrame(adverts_ok)
        # print(df.head())
