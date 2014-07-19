__author__ = 'Nick'
# Simple test for solar model

import pandas as pd
from calc_solar import *
from Solar import SolarModel, SolarOptimization
import os
from Common.AttributeTools.io import print_outputs

user = os.getenv('USERNAME')
projectPath = '\\.openmdao\\gui\\projects\\GeorgiaAquarium\\Energy\\Sources\\Solar\\solarAtl2010.csv'

sunpath =  'c:\\Users\\' + user + projectPath
sunData0 = pd.read_csv(sunpath, index_col=["date", "time"],parse_dates=["date"])
sunData = sunData0["irradiance"].values


def testSolarClean():
    calc_power(1.0, 1.0, 1.0, 1.0, 1.0, sunData)

def testSolarComp():
    sm = SolarModel()
    sm.execute()

def test_solar_non_neg():
    numPanels = calc_num_panels(148.0, 0.7)
    cost = calc_cost(0.7, 500, 300, numPanels)
    assert cost > 0
    assert numPanels % numPanels == 0

def test_solar_optimization():
    so = SolarOptimization()
    so.execute()

def run_print_test():
    comp = SolarModel()
    comp.execute()
    print_outputs(comp)