"""
   /Energy/Sources/Wind/Wind.py
"""

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_wind import calc_cost, calc_power
from Common.AttributeTools.io import print_outputs


class WindModel(Component):
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    turbineCount = Float(1.0, iotype='in', desc='turbine count')
    turbineRating = Float(1.0, iotype='in', desc='turbine power rating (kW)')
    turbineEff = Float(1.0, iotype='in', desc='turbine efficiency (percent)')
    windSpeedScalar = Float(1.0, iotype='in', desc='uncertainty around wind speed (scalar)')
    windCostPerWatt = Float(1.0, iotype='in', desc='wind cost per capacity ($/watt)')
    circuitLoss = Float(1.0, iotype='in', desc='circuit power loss (percent)')
    airDensity = Float(1.0, iotype='in', desc='air density (kg/m^3)')
    bladeLength = Float(1.0, iotype='in', desc='turbine blade length (m)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    windCapitalCost = Float(1.0, iotype='out', desc='investment cost ($)')

    # set up constants
    windDataTable = pd.read_csv(path + '\\windAtl.csv')
    windData = windDataTable["windSpeed"].values

    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.bladeLength,
            self.turbineEff,
            self.airDensity,
            self.turbineCount,
            self.circuitLoss,
            self.windData)

        # Calculate cost
        self.windCapitalCost = calc_cost(
            self.windCostPerWatt,
            self.turbineRating,
            self.turbineCount)


def run_tests():
    comp = WindModel()
    comp.execute()
    print_outputs(comp)


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()