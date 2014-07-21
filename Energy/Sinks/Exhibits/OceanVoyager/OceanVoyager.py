"""
   /Energy/Sinks/Exhibits/OceanVoyager/OceanVoyager.py
"""

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, Array

from Common.AttributeTools.io import print_outputs
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_protein_skimmer_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_sand_filter_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_power, calc_sand_power
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_cost, calc_sand_cost
from Common.Lighting.Lighting import LightingModel
from Common.Lighting.calc_lighting import Lights
from numpy import float as numpy_float
import numpy as np


class OceanVoyagerModel(Component):
    # set up inputs
    # protein skimmer model
    proteinRatedSpeed = Float(800.0, iotype='in', desc='electric pump speed rating')
    lossMultiplier = Float(20.0, iotype='in', desc='loss multiplier')
    proteinRatedEff = Float(0.6, iotype='in', desc='electric pump efficiency')
    ratedHead = Float(20.0, iotype='in', desc='electric pump rated head')
    ratedFlow = Float(1300.0, iotype='in', desc='electric pump rated flow')
    referenceArea = Float(0.1, iotype='in', desc='reference area')
    runSpeed = Float(800.0, iotype='in', desc='electric pump actual run speed')
    pumpModificationUnitCost = Float(3500.0, iotype='in', desc='electric pump modification cost')
    doProteinUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')

    # sand filter model
    pumpFlow = Float(1669.0, iotype='in', desc='electric pump rated flow')
    pumpRatedHead = Float(76.0, iotype='in', desc='electric pump rated head')
    pumpRatedRpm = Float(1074.0, iotype='in', desc='electric pump speed rating')
    pumpRunRpm = Float(1000.0, iotype='in', desc='electric pump actual run speed')
    pumpEff = Float(0.79, iotype='in', desc='electric pump efficiency')
    flowLossCoef = Float(3.54, iotype='in', desc='electric pump speed rating')
    heatExchFlowLossCoef = Float(5.06, iotype='in', desc='electric pump speed rating')
    heatExchValveOpen = Float(0.1, iotype='in', desc='loss multiplier')
    denitFLowLossCoef = Float(0.54, iotype='in', desc='electric pump efficiency')
    ozoneFlowLossCoef = Float(0.57, iotype='in', desc='electric pump rated head')
    ozoneValveOpen = Float(0.1, iotype='in', desc='electric pump rated flow')
    denitValveOpen = Float(0.1, iotype='in', desc='reference area')
    deaerationFlowLossCoef = Float(0.3, iotype='in', desc='electric pump actual run speed')
    doSandUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')

    # lighting model
    numBulbs = Float(1.0, iotype='in', desc='number of bulbs to replace')

    # set up outputs
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
    yearlykWhNominal = Float(1.0, iotype='out', desc='yearly power usage for lighting (nominal)')
    yearlykWh = Float(1.0, iotype='out', desc='yearly power usage for lighting (new configuration)')
    totalPowerUsed = Float(1.0, iotype='out', desc='yearly power output')

    # cost
    proteinCapitalCost = Float(153000.0, iotype='out', desc='cost of modification')
    sandCapitalCost = Float(162000.0, iotype='out', desc='cost of modification')
    yearlyHydraulicCapitalCost = Array(np.array([[360000.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0]]),
                                 dtype=numpy_float, shape=(1, 10), iotype='out',
                                 desc='hydraulic costs for 10 years')
    hydraulicCapitalCost = Float(315000.0, iotype='out', desc='cost of modification')

    # lighting nominal
    recurringCostsNominal = Array(np.array([[0.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0]]), dtype=numpy_float,
                                  shape=(1, 10), iotype='out', desc='lighting recurring costs for 10 years')
    # lighting new costs
    recurringCosts = Array(np.array([[0.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0, 0.0, 6000, 0.0]]), dtype=numpy_float,
                           shape=(1, 10), iotype='out', desc='lighting recurring costs for 10 years, new config')

    # set up constants
    # protein skimmer
    numProteinPumps = 34
    currentProteinPumpKw = 580.95
    currentProteinRatedSpeed = 1180
    currentProteinRatedFlow = 1960
    currentProteinRatedEff = 69
    currentProteinRatedHead = 31
    currentProteinCircuitLoss = 150

    # sand filter
    numSandPumps = 36
    currentSandPumpKw = 1230.24
    currentSandRatedSpeed = 1006
    currentSandRatedFlow = 1316
    currentSandRatedEff = 73
    currentSandRatedHead = 53
    currentSandCircuitLoss = 3.54
    currentSandHxCircuitLoss = 5.06
    currentSandOzCircuitLoss = 0.57
    currentSandDnCircuitLoss = 0.54
    currentSandDatCircuitLoss = 0.33

    # lighting
    currentNumLights = 40.0
    currentBulbWatts = 1000.0  # watts
    currentBulbCost = 180.0    # dollars
    currentBulbLife = 10000    # hours
    hoursPerDay = 12           # hours lights are on each day
    scaleRatio = 1.5           # number of new lights required per old
    newLightWatts = 120
    newLightCost = 712
    newLightLife = 50000


    # primary model init
    def __init__(self):
        '''
        Extend the OpenMDAO component init method only so that we don't have to reload the surrogate model files each
        time it is executed. This might be considered bad practice, but is necessary to reduce run time. There could
        be a better way to avoid this problem.

        :return: Initialized OpenMDAO component object with protein and sand surrogate models loaded
        '''
        # ToDo: See if there is a better way to initialize the surrogate without having to extend the constructor

        super(OceanVoyagerModel, self).__init__()

        # Protein Skimmers Surrogate Model
        self.protein_surrogate = init_protein_skimmer_surrogate()

        # Sand Filters Surrogate Model
        self.sand_surrogate = init_sand_filter_surrogate()

        # Init light models
        lsOld = Lights([self.currentNumLights], [1], [self.currentBulbLife], [self.currentBulbCost],
                       [self.currentBulbLife], [self.hoursPerDay], [True]) # Old Lights config
        lsNew = Lights([self.currentNumLights], [self.scaleRatio], [self.newLightWatts], [self.newLightCost],
                       [self.newLightLife], [self.hoursPerDay], [False]) # New Lights config
        self.lightModel = LightingModel(lsNew, lsOld)
        self.lightModel.execute()

    # primary model method
    def execute(self):
        '''
        The method that OpenMDAO requires that the behavior of the model be developed in. At each model execution,
        OpenMDAO will write new values into the model's inputs, then will call this execute method. After the
        execution is complete, it will read total power and total initial capital cost information from it.

        :return: None
        '''

        # Add all protein skimmer related inputs into a list for input into surrogate
        inputsProtein = [self.proteinRatedSpeed, self.lossMultiplier, self.proteinRatedEff, self.ratedHead,
                         self.ratedFlow, self.referenceArea, self.runSpeed]

        # Add all sand filter related inputs into a list for input into surrogate
        inputsSand = [self.pumpFlow, self.pumpRatedHead, self.pumpRatedRpm, self.pumpRunRpm,self.pumpEff,
                      self.flowLossCoef, self.heatExchFlowLossCoef, self.heatExchValveOpen, self.denitFLowLossCoef,
                      self.ozoneFlowLossCoef, self.ozoneValveOpen, self.denitValveOpen, self.deaerationFlowLossCoef]

        # Calculations for protein skimmers
        # This calculation is dependent on whether or not we'd like to do an upgrade. The upgrade is essentially the
        # controlling design variable, while the actual hydraulic-specific variables are only relevant if we perform
        # the upgrade. Otherwise, we set the output values to their default.
        if self.doProteinUpgrade == 1.0:
            # Calculate protein performance attributes
            self.totalPowerProtein, \
            self.proteinHead, \
            self.totalFlowProtein = calc_protein_power(self.protein_surrogate, inputsProtein, self.numProteinPumps)

            # Calculate protein cost
            self.proteinCapitalCost = calc_protein_cost(self.numProteinPumps, self.pumpModificationUnitCost,
                                                        self.lossMultiplier, self.currentProteinCircuitLoss,
                                                        self.proteinRatedEff, self.currentProteinRatedEff,
                                                        self.proteinRatedSpeed, self.currentProteinRatedSpeed,
                                                        self.ratedFlow, self.currentProteinRatedFlow,
                                                        self.ratedHead, self.currentProteinRatedHead)
        else:
            # No upgrade, set outputs to original values
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
            self.sandCapitalCost = calc_sand_cost(self.numSandPumps, self.pumpModificationUnitCost,
                                                  self.pumpRatedRpm, self.currentSandRatedSpeed,
                                                  self.pumpFlow, self.currentSandRatedFlow,
                                                  self.pumpEff, self.currentSandRatedEff,
                                                  self.pumpRatedHead, self.currentSandRatedHead,
                                                  self.flowLossCoef, self.currentSandCircuitLoss,
                                                  self.heatExchFlowLossCoef, self.currentSandHxCircuitLoss,
                                                  self.ozoneFlowLossCoef, self.currentSandOzCircuitLoss,
                                                  self.denitFLowLossCoef, self.currentSandDnCircuitLoss,
                                                  self.deaerationFlowLossCoef, self.currentSandDatCircuitLoss)
        else:
            self.sandFilterFlow = 800.0
            self.totalFlowSand = 61000.0
            self.heatExchFlow1 = 1000.0
            self.heatExchFlow2 = 1000.0
            self.denitFlow = 8000.0
            self.bypassFlow = 45500.0
            self.totalPowerSand = self.currentSandPumpKw * 24 * 365
            self.sandCapitalCost = 0.0


        # Execute lighting model
        self.lightModel.numBulbs = self.numBulbs
        self.lightModel.execute()
        self.recurringCostsNominal = self.lightModel.nominalRecurring
        self.yearlykWhNominal = self.lightModel.nominalkWh
        self.yearlykWh = self.lightModel.yearlykWh

        # Total calculations
        # Here we are aggregating up all of the modeled elements of the OceanVoyager exhibit and combining them into
        # a single set of outputs. If more components were modeled, this is where the aggregation of the various
        # attributes would be performed.
        self.totalPowerUsed = self.totalPowerProtein + self.totalPowerSand + self.lightModel.yearlykWh

        self.yearlyHydraulicCapitalCost = self.recurringCosts
        self.hydraulicCapitalCost = self.yearlyHydraulicCapitalCost[0,0] + self.proteinCapitalCost + \
                                    self.sandCapitalCost

if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    from test_ocean_voyager import test_ov_openmdao_model
    test_ov_openmdao_model()