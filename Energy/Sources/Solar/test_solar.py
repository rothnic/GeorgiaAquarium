__author__ = 'Nick'
# Simple test for solar model


import pandas as pd

from Energy.Sources.Solar.calc_solar import calc_power
from Energy.Sources.Solar.Solar import SolarModel

path = "C:\Users\Nick\.openmdao\gui\projects\GeorgiaAquarium\Energy\Sources\Solar\solarAtl2010.csv"
sunData0 = pd.read_csv(path,
                       index_col=["date", "time"],
                       parse_dates=["date"])
sunData = sunData0["irradiance"].values


def testSolarClean():
    calc_power(1.0, 1.0, 1.0, 1.0, 1.0, sunData)

def testSolarComp():
    sm = SolarModel()
    sm.execute()