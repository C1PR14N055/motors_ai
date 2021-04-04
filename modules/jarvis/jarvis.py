from ..utils import Tools
from ..storage import Shelf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Jarvis():
    def __init__(self):
        self.shelf = Shelf()
        adverts_ok, _ = self.shelf.unpickle_adverts()

        df = pd.DataFrame([x.__dict__ for x in adverts_ok])
        pd.set_option('max_columns', None)
        print(df.head())

        bins = np.arange(0, 600, 100)
        groups = df.groupby(pd.cut(df['HorsePower'], bins)).mean()
        groups['Price'].plot.line()
        plt.show(block=True)
        # time.sleep(10)
