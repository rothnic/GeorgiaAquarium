"""
   /Energy/Sinks/Exhibits/OceanVoyager/OceanVoyager.py
"""

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
from Energy.Sinks.Exhibits.OceanVoyager.calc_ocean_voyager import init_surrogate, calc_power, calc_cost

from Common.FfnetSurrogate.FfnetSurrogate import FfnetSurrogate


class OceanVoyagerModel(Component):
    # set up inputs
    ratedSpeed = Float(800.0, iotype='in', desc='electric pump speed rating')
    lossMultiplier = Float(20.0, iotype='in', desc='loss multiplier')
    ratedEff = Float(0.6, iotype='in', desc='electric pump efficiency')
    ratedHead = Float(20.0, iotype='in', desc='electric pump rated head')
    ratedFlow = Float(1300.0, iotype='in', desc='electric pump rated flow')
    referenceArea = Float(0.1, iotype='in', desc='reference area')
    runSpeed = Float(1600.0, iotype='in', desc='electric pump actual run speed')

    # set up outputs
    totalPowerUsed = Float(1.0, iotype='out', desc='yearly power output')
    headOut = Float(1.0, iotype='out', desc='simulated head')
    totalFlow = Float(1.0, iotype='out', desc='simulated head')
    hydraulicCapitalCost = Float(1.0, iotype='out', desc='cost of modification')

    # set up constants
    numPumps = 34
    currentSandPumpKw = 1230.24

    def __init__(self):
        super(OceanVoyagerModel, self).__init__()

        self.surrogate = init_surrogate()


    def execute(self):
        # Initial setup

        inputs = [self.ratedSpeed, self.lossMultiplier, self.ratedEff, self.ratedHead,
                  self.ratedFlow, self.referenceArea, self.runSpeed]

        self.totalPowerUsed, self.headOut, self.totalFlow = calc_power(self.surrogate,
                                                                       inputs,
                                                                       self.numPumps)

        self.hydraulicCapitalCost = calc_cost()


if __name__=="__main__":
    comp = OceanVoyagerModel()
    comp.execute()
    print comp.totalPowerUsed
    print comp.headOut
    print comp.totalFlow
    print comp.hydraulicCapitalCost