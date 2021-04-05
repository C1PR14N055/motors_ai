from core import Config
from ..utils import Tools
from ..storage import Shelf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sea
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


class Jarvis():
    def __init__(self):
        self.shelf = Shelf()
        self.adverts_ok, self.adverts_err = self.shelf.unpickle_adverts()
        self.dataframe = pd.DataFrame([x.__dict__ for x in self.adverts_ok])
        self.scale = None
        self.model = None
        sea.set()

        # safety trim
        self.dataframe.columns = self.dataframe.columns.str.strip()
        # show dataframe head all columns
        pd.set_option('max_columns', None)
        Tools.log('** Available dataframes **')
        Tools.log(self.dataframe.head())

    def plot_years(self):
        # vs price scale
        ys_bins = np.arange(2000, 2022, 2)
        ys = self.dataframe.groupby(
            pd.cut(self.dataframe['FabricationYear'], ys_bins)
        ).median()
        ys.plot(x='FabricationYear', y='Price')
        plt.show(block=True)

    def plot_hp(self):
        # vs price
        hp_bins = np.arange(50, 250, 30)
        hp = self.dataframe.groupby(
            pd.cut(self.dataframe['HorsePower'], hp_bins)
        ).mean()
        hp[['HorsePower', 'Price']].plot.line(
            x='HorsePower', y='Price'
        )
        plt.show(block=True)

    # TODO: save model and scale
    def build_model(self):
        self.scale = StandardScaler()

        # important features selection
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

        # to be predicted
        y = self.dataframe['Price']

        '''
        The fit_transform method calculates the mean and
        variance of each of the features
        present in our data, transforming all the
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
              ] = self.scale.fit_transform(
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

        # Scaled data
        Tools.log('** Scaled data **\n{}'.format(X))

        '''
        Single Price prediction with Ordinary List Squares
        Data is normaziled (0, 1) (True) (False)
        Get rid of null features

        Ecuation:
        price = [ a + B1 * mileage + B2 * age + ... + Bx * n ]
        Measures fit with r-squared

        Example:
        statsmodel.OLS(predict, featuresVars).fit() // fits data to OLS model
        '''
        # log missing feature count
        Tools.log('** Null feature count **\n{} '.format(X.isnull().sum()))

        # fit model
        self.model = sm.OLS(y, X, missing='drop').fit()
        # log model summary
        Tools.log('*** Model Sumary: ***\n{}'.format(
            self.model.summary()
        ))

    def predict(self, car):
        scaled = self.scale.transform([car])
        predicted = self.model.predict(scaled[0])
        return predicted
