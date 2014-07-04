"""
   /Energy/Sources/Tribo/Tribo.py
"""

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_tribo import calc_cost, calc_power


class TriboModel(Component):
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    tileCount = Float(1.0, iotype='in', desc='turbine count')
    pedStepsPerTile = Float(1.0, iotype='in', desc='turbine power rating (kW)')
    triboEff = Float(1.0, iotype='in', desc='turbine efficiency (percent)')
    triboUnitCost = Float(1.0, iotype='in', desc='uncertainty around tribo speed (scalar)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    triboCapitalCost = Float(1.0, iotype='out', desc='investment cost ($)')

    # set up constants
    triboDataTable = pd.read_csv(path + '\\triboAtl.csv')
    triboData = triboDataTable["triboSpeed"].values

    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.bladeLength,
            self.turbineEff,
            self.airDensity,
            self.turbineCount,
            self.circuitLoss,
            self.triboData)

        # Calculate cost
        self.triboCapitalCost = calc_cost(
            self.triboCostPerWatt,
            self.turbineRating,
            self.turbineCount)