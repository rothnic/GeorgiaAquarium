"""
   /Energy/Sources/Solar/Solar.py
"""

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, Int

from calc_solar import *

class SolarModel(Component):
    # set up inputs
    panelRating = Float(0.0, iotype='in', desc='panel rating')
    panelEff = Float(0.0, iotype='in', desc='panel efficiency')
    sunRadianceScalar = Float(0.0, iotype='in', desc='uncertainty around radiance')
    numPanels = Int(0.0, iotype='in', desc='number of panels')
    solarCostPerWatt = Float(0.0, iotype='in', desc='solar cost')
    batteryCost = Float(0.0, iotype='in', desc='cost of batteries')
    circuitLoss = Float(0.0, iotype='in', desc='circuit power loss')

    # set up outputs
    # solarSurfaceArea = Float(0.0, iotype='out', desc='surface area')
    totalkWh = Float(0.0, iotype='out', desc='yearly power output')
    solarCapitalCost = Float(0.0, iotype='out', desc='investment cost')


    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.panelRating,
            self.panelEff,
            self.sunRadianceScalar,
            self.numPanels,
            self.circuitLoss)

        # Calculate cost
        self.solarCapitalCost = calc_cost(
            self.solarCostPerWatt,
            self.batteryCost)