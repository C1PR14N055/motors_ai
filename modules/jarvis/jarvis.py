from core import Config
from ..utils import Tools
from ..storage import Shelf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class Jarvis():
    def __init__(self):
        self.shelf = Shelf()
        self.adverts_ok, self.adverts_err = self.shelf.unpickle_adverts()
        self.dataframe = pd.DataFrame([x.__dict__ for x in self.adverts_ok])
        # safety trim
        self.dataframe.columns = self.dataframe.columns.str.strip()
        # show dataframe head all columns
        pd.set_option('max_columns', None)
        Tools.log(self.dataframe.head())

    def plot_most_expensive(self):
        # most expensive brands bar chart
        self.dataframe.sort_values('Price').plot.bar('BrandID', 'Price')

    def plot_years(self):
        # years plot
        ys_bins = np.arange(2000, 2021, 1)
        ys = self.dataframe.groupby(
            pd.cut(self.dataframe['FabricationYear'], ys_bins)
        ).median()
        ys.plot(x='FabricationYear', y='Price')

    def plot_hp(self):
        # horse power plot
        hp_bins = np.arange(50, 270, 25)
        hp = self.dataframe.groupby(
            pd.cut(self.dataframe['HorsePower'], hp_bins)
        ).mean()
        hp[['HorsePower', 'Price']].plot.bar(x='HorsePower', y='Price')

        plt.show(block=True)

    def ml(self):
        import statsmodels.api as sm
        from sklearn.preprocessing import StandardScaler
        scale = StandardScaler()

        X = self.dataframe[['BrandID', 'FabricationYear', 'BrandModelID']]
        y = self.dataframe['Price']

        X.loc[:,
              ['BrandID', 'FabricationYear', 'BrandModelID']
              ] = scale.fit_transform(
            X[['BrandID', 'FabricationYear', 'BrandModelID']].values
        )

        print(X)
        est = sm.OLS(y, X).fit()
        est.summary()
