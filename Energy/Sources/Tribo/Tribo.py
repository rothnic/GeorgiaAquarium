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
    tileCount = Float(1.0, iotype='in', desc='number of tiles')
    pedStepsPerTile = Float(1.0, iotype='in', desc='expected steps per tile')
    triboEff = Float(1.0, iotype='in', desc='tribo efficiency (percent)')
    triboUnitCost = Float(1.0, iotype='in', desc='unit cost of a single tile')
    tribokWh = Float(1.0, iotype='in', desc='power produced per step (kWh)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    triboCapitalCost = Float(1.0, iotype='out', desc='investment cost ($)')


    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.tileCount,
            self.pedStepsPerTile,
            self.triboEff,
            self.tribokWh)

        # Calculate cost
        self.triboCapitalCost = calc_cost(
            self.triboUnitCost,
            self.tileCount)