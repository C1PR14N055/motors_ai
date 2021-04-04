from core import Config
from ..utils import Tools
from ..storage import Shelf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Jarvis():
    def __init__(self):
        self.shelf = Shelf()
        self.adverts_ok, self.adverts_err = self.shelf.unpickle_adverts()
        self.dataframe = pd.DataFrame([x.__dict__ for x in self.adverts_ok])
        # safety trim
        self.dataframe.columns = self.dataframe.columns.str.strip()
        # show dataframe head all columns
        pd.set_option('max_columns', None)
        Tools.log('** Available dataframes **')
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

    def stats(self):
        import statsmodels.api as sm
        from sklearn.preprocessing import StandardScaler
        scale = StandardScaler()

        # usable dataframe values
        X = self.dataframe.loc[:,
                               (
                                   'BrandID',
                                   'BrandModelID',
                                   'FabricationYear',
                                   'CityID',
                                   'PollutionNormID',
                                   'CountryID',
                                   'Status',
                                   'Matriculated',
                                   'ServiceBook',
                                   'ParticleFilter',
                                   'MetallicColor',
                                   'FirstOwner',
                                   'NoAccidents',
                                   'Tuning',
                                   'Negotiable',
                                   'CubicCapacity',
                                   'KmNumber',
                                   'HorsePower',
                                   'DoorsNumber',
                               )
                               ]

        # to be predicted dataframe values
        y = self.dataframe['Price']

        '''
        The fit_transform method calculates the mean and
        variance of each of the features
        present in our data transforming all the
        features using the respective mean and variance
        '''
        X.loc[:,
              (
                  'BrandID',
                  'BrandModelID',
                  'FabricationYear',
                  'CityID',
                  'PollutionNormID',
                  'CountryID',
                  'Status',
                  'Matriculated',
                  'ServiceBook',
                  'ParticleFilter',
                  'MetallicColor',
                  'FirstOwner',
                  'NoAccidents',
                  'Tuning',
                  'Negotiable',
                  'CubicCapacity',
                  'KmNumber',
                  'HorsePower',
                  'DoorsNumber',
              )
              ] = scale.fit_transform(
            X[[
                'BrandID',
                'BrandModelID',
                'FabricationYear',
                'CityID',
                'PollutionNormID',
                'CountryID',
                'Status',
                'Matriculated',
                'ServiceBook',
                'ParticleFilter',
                'MetallicColor',
                'FirstOwner',
                'NoAccidents',
                'Tuning',
                'Negotiable',
                'CubicCapacity',
                'KmNumber',
                'HorsePower',
                'DoorsNumber',
            ]].values
        )

        null_nr = X.isnull().sum()
        Tools.log('** Null data count: {} **'.format(null_nr))
        Tools.log('X: {}'.format(X))
        estimate = sm.OLS(y, X, missing='drop').fit()
        Tools.log('Est: {}'.format(estimate))
        summary = estimate.summary()
        Tools.log('Est. summary: {}'.format(summary))
