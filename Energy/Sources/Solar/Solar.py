"""
   /Energy/Sources/Solar/Solar.py
"""

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_solar import calc_cost, calc_power, calc_num_panels
from Common.AttributeTools.io import print_outputs


class SolarModel(Component):
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    panelRating = Float(280.0, iotype='in', desc='panel rating')
    panelEff = Float(0.17, iotype='in', desc='panel efficiency')
    sunRadianceScalar = Float(1.0, iotype='in', desc='uncertainty around radiance')
    surfaceArea = Float(558.0, iotype='in', desc='number of panels')
    solarCostPerWatt = Float(1.50, iotype='in', desc='solar cost')
    batteryCost = Float(0.0, iotype='in', desc='cost of batteries')
    circuitLoss = Float(0.7, iotype='in', desc='circuit power loss')

    # set up outputs
    totalkWh = Float(110000.0, iotype='out', desc='yearly power output')
    solarCapitalCost = Float(150000.0, iotype='out', desc='investment cost')

    # set up constants
    panelSize = 1.42
    maxSurfaceArea = 1000.0 # Square meters
    sunDataTable = pd.read_csv(path + '\\solarAtl2010.csv')
    sunData = sunDataTable["irradiance"].values

    def execute(self):
        # Initial setup
        numPanels = calc_num_panels(self.surfaceArea, self.panelSize)
        self.solarCostPerWatt = (-68.33333 + 7.5 * self.panelEff) * self.surfaceArea * 0.027945

        # Calculate power
        self.totalkWh = calc_power(
            self.panelRating,
            self.panelEff,
            self.sunRadianceScalar,
            self.surfaceArea,
            self.circuitLoss,
            self.sunData)

        # Calculate cost
        self.solarCapitalCost = calc_cost(
            self.solarCostPerWatt,
            self.panelRating,
            numPanels)


def run_tests():
    comp = SolarModel()
    comp.execute()
    print_outputs(comp)


if __name__ == "__main__":
    from test_solar import *
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()
    testSolarClean()
    testSolarComp()
    test_solar_non_neg()
