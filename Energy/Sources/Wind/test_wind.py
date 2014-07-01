__author__ = 'Nick'
# Simple test for solar model


import pandas as pd

from Energy.Sources.Wind.calc_wind import calc_power
from Energy.Sources.Wind.Wind import WindModel

path = "C:\Users\Nick\.openmdao\gui\projects\GeorgiaAquarium\Energy\Sources\Wind\windAtl.csv"
windDataTable = pd.read_csv(path)
windData = windDataTable["windSpeed"].values


def testWindPowerFunction():
    calc_power(1.0, 1.0, 1.0, 1.0, 1.0, windData)


def testWindComponent():
    wm = WindModel()
    wm.execute()