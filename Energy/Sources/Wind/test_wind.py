__author__ = 'Nick'
# Simple test for solar model


import pandas as pd

from Energy.Sources.Wind.calc_wind import calc_power
from Energy.Sources.Wind.Wind import WindModel, WindOptimization
from Common.AttributeTools.io import get_output_values, print_outputs

path = "C:\Users\Nick\.openmdao\gui\projects\GeorgiaAquarium\Energy\Sources\Wind\windAtl.csv"
windDataTable = pd.read_csv(path)
windData = windDataTable["windSpeed"].values


def test_wind_power_calc():
    calc_power(1.0, 1.0, 1.0, 1.0, 1.0, windData)


def test_wind_component():
    wm = WindModel()
    wm.execute()
    outputs = get_output_values(wm)
    for key in outputs:
        assert outputs[key] > 0


def run_print_test():
    comp = WindModel()
    comp.execute()
    print_outputs(comp)


def test_wind_optimization():
    wo = WindOptimization()
    wo.execute()