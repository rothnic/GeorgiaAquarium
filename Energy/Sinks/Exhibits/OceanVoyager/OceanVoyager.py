"""
   /Energy/Sinks/Exhibits/OceanVoyager/OceanVoyager.py
"""

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from Common.AttributeTools.io import print_outputs

from Energy.Sinks.Exhibits.OceanVoyager.calc_ocean_voyager import init_surrogate, calc_power, calc_cost


class OceanVoyagerModel(Component):
    # set up inputs
    ratedSpeed = Float(800.0, iotype='in', desc='electric pump speed rating')
    lossMultiplier = Float(20.0, iotype='in', desc='loss multiplier')
    ratedEff = Float(0.6, iotype='in', desc='electric pump efficiency')
    ratedHead = Float(20.0, iotype='in', desc='electric pump rated head')
    ratedFlow = Float(1300.0, iotype='in', desc='electric pump rated flow')
    referenceArea = Float(0.1, iotype='in', desc='reference area')
    runSpeed = Float(800.0, iotype='in', desc='electric pump actual run speed')
    pumpModificationUnitCost = Float(8000.0, iotype='in', desc='electric pump modification cost')
    numPumpRetrofits = Float(34.0, iotype='in', desc='electric pump modification cost')

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

        # Calculate performance attributes
        self.totalPowerUsed, self.headOut, self.totalFlow = calc_power(
            self.surrogate,
            inputs,
            self.numPumps)

        # Calculate the cost
        self.hydraulicCapitalCost = calc_cost(self.numPumpRetrofits, self.pumpModificationUnitCost)


def run_tests():
    # Module test routine, only executes when this python is ran independently
    # For example, using Pycharm, right click while editing and select Run
    comp = OceanVoyagerModel()
    comp.execute()
    print_outputs(comp)

if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()