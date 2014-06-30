"""
   /Energy/Sources/Solar/Solar.py
"""

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_solar import calc_cost, calc_power, calc_num_panels


class SolarModel(Component):
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    panelRating = Float(1.0, iotype='in', desc='panel rating')
    panelEff = Float(1.0, iotype='in', desc='panel efficiency')
    sunRadianceScalar = Float(1.0, iotype='in', desc='uncertainty around radiance')
    surfaceArea = Float(1.0, iotype='in', desc='number of panels')
    solarCostPerWatt = Float(1.0, iotype='in', desc='solar cost')
    batteryCost = Float(1.0, iotype='in', desc='cost of batteries')
    circuitLoss = Float(1.0, iotype='in', desc='circuit power loss')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output')
    solarCapitalCost = Float(1.0, iotype='out', desc='investment cost')

    # set up constants
    panelSize = 0.7
    sunDataTable = pd.read_csv(path + '\\solarAtl2010.csv',
                           index_col=["date", "time"],
                           parse_dates=["date"])
    sunData = sunDataTable["irradiance"].values

    def execute(self):
        # Initial setup
        numPanels = calc_num_panels(self.surfaceArea, self.panelSize)

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