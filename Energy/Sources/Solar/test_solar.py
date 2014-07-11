__author__ = 'Nick'
# Simple test for solar model


import pandas as pd

from Energy.Sources.Solar.calc_solar import *
from Energy.Sources.Solar.Solar import SolarModel, SolarOptimization
from Common.AttributeTools.io import print_outputs

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

def test_solar_non_neg():
    numPanels = calc_num_panels(148.0, 0.7)
    cost = calc_cost(1.17, 183, numPanels)
    assert cost > 0
    assert numPanels % numPanels == 0

def test_solar_optimization():
    so = SolarOptimization()
    so.execute()

def run_print_test():
    comp = SolarModel()
    comp.execute()
    print_outputs(comp)