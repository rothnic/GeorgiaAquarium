"""
   /Energy/Sinks/Exhibits/OceanVoyager/OceanVoyager.py
"""

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, Enum

from Common.AttributeTools.io import print_outputs
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_protein_skimmer_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_sand_filter_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_power, calc_sand_power
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_cost, calc_sand_cost


class OceanVoyagerModel(Component):
    # set up inputs
    proteinRatedSpeed = Float(800.0, iotype='in', desc='electric pump speed rating')
    lossMultiplier = Float(20.0, iotype='in', desc='loss multiplier')
    proteinRatedEff = Float(0.6, iotype='in', desc='electric pump efficiency')
    ratedHead = Float(20.0, iotype='in', desc='electric pump rated head')
    ratedFlow = Float(1300.0, iotype='in', desc='electric pump rated flow')
    referenceArea = Float(0.1, iotype='in', desc='reference area')
    runSpeed = Float(800.0, iotype='in', desc='electric pump actual run speed')
    pumpModificationUnitCost = Float(4500.0, iotype='in', desc='electric pump modification cost')
    pumpFlow = Float(1300.0, iotype='in', desc='electric pump rated flow')
    pumpRatedHead = Float(40.0, iotype='in', desc='electric pump rated head')
    pumpRatedRpm = Float(1000.0, iotype='in', desc='electric pump speed rating')
    pumpRunRpm = Float(1000.0, iotype='in', desc='electric pump actual run speed')
    pumpEff = Float(0.6, iotype='in', desc='electric pump efficiency')
    flowLossCoef = Float(0.1, iotype='in', desc='electric pump speed rating')
    heatExchFlowLossCoef = Float(0.1, iotype='in', desc='electric pump speed rating')
    heatExchValveOpen = Float(0.1, iotype='in', desc='loss multiplier')
    denitFLowLossCoef = Float(0.1, iotype='in', desc='electric pump efficiency')
    ozoneFlowLossCoef = Float(0.1, iotype='in', desc='electric pump rated head')
    ozoneValveOpen = Float(0.1, iotype='in', desc='electric pump rated flow')
    denitValveOpen = Float(0.1, iotype='in', desc='reference area')
    deaerationFlowLossCoef = Float(2.0, iotype='in', desc='electric pump actual run speed')
    doProteinUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')
    doSandUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')


    # Set up outputs
    # potential constraints
    proteinHead = Float(25.0, iotype='out', desc='simulated head')
    totalFlowSand = Float(63000.0, iotype='out', desc='total gallons per minute sand filters')
    totalFlowProtein = Float(1.0, iotype='out', desc='total gallons per minute protein skimmers')
    heatExchFlow1 = Float(1000.0, iotype='out', desc='simulated head')
    heatExchFlow2 = Float(1000.0, iotype='out', desc='simulated head')
    denitFlow = Float(8000.0, iotype='out', desc='simulated head')
    bypassFlow = Float(45500.0, iotype='out', desc='simulated head')
    sandFilterFlow = Float(800.0, iotype='out', desc='flow through one of the sand filters')

    # power
    totalPowerSand = Float(1350.0, iotype='out', desc='yearly power used for sand filters')
    totalPowerProtein = Float(1.0, iotype='out', desc='yearly power used for protein skimmers')
    totalPowerUsed = Float(1.0, iotype='out', desc='yearly power output')

    # cost
    proteinCapitalCost = Float(153000.0, iotype='out', desc='cost of modification')
    sandCapitalCost = Float(162000.0, iotype='out', desc='cost of modification')
    hydraulicCapitalCost = Float(315000.0, iotype='out', desc='cost of modification')

    # set up constants
    numProteinPumps = 34
    numSandPumps = 36
    currentSandPumpKw = 1230.24
    currentProteinPumpKw = 580.95

    def __init__(self):
        super(OceanVoyagerModel, self).__init__()

        # Protein Skimmers Surrogate Model
        self.protein_surrogate = init_protein_skimmer_surrogate()

        # Sand Filters Surrogate Model
        self.sand_surrogate = init_sand_filter_surrogate()


    def execute(self):
        # Initial setup

        # Add all protein skimmer related inputs into a list for input into surrogate
        inputsProtein = [self.proteinRatedSpeed, self.lossMultiplier, self.proteinRatedEff, self.ratedHead,
                         self.ratedFlow, self.referenceArea, self.runSpeed]

        # Add all sand filter related inputs into a list for input into surrogate
        inputsSand = [self.pumpFlow, self.pumpRatedHead, self.pumpRatedRpm, self.pumpRunRpm,self.pumpEff,
                      self.flowLossCoef, self.heatExchFlowLossCoef, self.heatExchValveOpen, self.denitFLowLossCoef,
                      self.ozoneFlowLossCoef, self.ozoneValveOpen, self.denitValveOpen, self.deaerationFlowLossCoef]

        # Calculations for protein skimmers
        if self.doProteinUpgrade == 1.0:
            # Calculate protein performance attributes
            self.totalPowerProtein, \
            self.proteinHead, \
            self.totalFlowProtein = calc_protein_power(self.protein_surrogate, inputsProtein, self.numProteinPumps)

            # Calculate protein cost
            self.proteinCapitalCost = calc_protein_cost(self.numProteinPumps, self.pumpModificationUnitCost)
        else:
            self.proteinHead = 25.0
            self.totalFlowProtein = 63000.0
            self.totalPowerProtein = self.currentProteinPumpKw * 24 * 365
            self.proteinCapitalCost = 0.0

        # Calculations for sand filters
        # This calculation is dependent on whether or not we'd like to do an upgrade. The upgrade is essentially the
        # controlling design variable, while the actual hydraulic-specific variables are only relevant if we perform
        # the upgrade. Otherwise, we set the output values to their default.
        if self.doSandUpgrade == 1.0:
            # Calculate sand filter performance attributes
            self.totalPowerSand, \
            self.sandFilterFlow, \
            self.heatExchFlow1, \
            self.heatExchFlow2, \
            self.denitFlow, \
            self.bypassFlow, \
            self.totalFlowSand = calc_sand_power(self.sand_surrogate, inputsSand, self.numSandPumps)

            # Calculate sand filter cost
            self.sandCapitalCost = calc_sand_cost(self.numSandPumps, self.pumpModificationUnitCost)
        else:
            self.sandFilterFlow = 800.0
            self.totalFlowSand = 61000.0
            self.heatExchFlow1 = 1000.0
            self.heatExchFlow2 = 1000.0
            self.denitFlow = 8000.0
            self.bypassFlow = 45500.0
            self.totalPowerSand = self.currentSandPumpKw * 24 * 365
            self.sandCapitalCost = 0.0

        # Total calculations
        # Here we are aggregating up all of the modeled elements of the OceanVoyager exhibit and combining them into
        # a single set of outputs. If more components were modeled, this is where the aggregation of the various
        # attributes would be performed.
        self.totalPowerUsed = self.totalPowerProtein + self.totalPowerSand
        self.hydraulicCapitalCost = self.proteinCapitalCost + self.sandCapitalCost


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