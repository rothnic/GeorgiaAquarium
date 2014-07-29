"""
   /Energy/Sinks/Exhibits/OceanVoyager/OceanVoyager.py
"""

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float, Array
from openmdao.lib.doegenerators.optlh import LatinHypercube
from openmdao.lib.drivers.doedriver import DOEdriver

from Common.AttributeTools.io import print_outputs
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_protein_skimmer_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import init_sand_filter_surrogate
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_power, calc_sand_power
from Energy.Sinks.Exhibits.OceanVoyager.calc_hydraulic import calc_protein_cost, calc_sand_cost
from openmdao.lib.casehandlers.api import CSVCaseRecorder
from Common.Lighting.Lighting import LightingModel
from Common.Lighting.calc_lighting import Lights
from numpy import float as numpy_float
from pyopt_driver.pyopt_driver import pyOptDriver
import numpy as np


class OceanVoyagerModel(Component):
    # set up inputs
    # protein skimmer model
    proteinRatedSpeed = Float(1590.0, iotype='in', desc='electric pump speed rating')
    lossMultiplier = Float(132.0, iotype='in', desc='loss multiplier')
    proteinRatedEff = Float(0.696, iotype='in', desc='electric pump efficiency')
    ratedHead = Float(29.2, iotype='in', desc='electric pump rated head')
    ratedFlow = Float(1668.0, iotype='in', desc='electric pump rated flow')
    referenceArea = Float(0.1, iotype='in', desc='reference area')
    runSpeed = Float(1590.0, iotype='in', desc='electric pump actual run speed')
    pumpModificationUnitCost = Float(3500.0, iotype='in', desc='electric pump modification cost')
    doProteinUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')

    # sand filter model
    pumpFlow = Float(1315.0, iotype='in', desc='electric pump rated flow')
    pumpRatedHead = Float(53.00, iotype='in', desc='electric pump rated head')
    pumpRatedRpm = Float(1006.0, iotype='in', desc='electric pump speed rating')
    pumpRunRpm = Float(1288.0, iotype='in', desc='electric pump actual run speed')
    pumpEff = Float(0.73, iotype='in', desc='electric pump efficiency')
    flowLossCoef = Float(3.54, iotype='in', desc='electric pump speed rating')
    heatExchFlowLossCoef = Float(5.06, iotype='in', desc='electric pump speed rating')
    heatExchValveOpen = Float(0.99, iotype='in', desc='loss multiplier')
    denitFlowLossCoef = Float(0.54, iotype='in', desc='electric pump efficiency')
    ozoneFlowLossCoef = Float(0.56, iotype='in', desc='electric pump rated head')
    ozoneValveOpen = Float(0.34, iotype='in', desc='electric pump rated flow')
    denitValveOpen = Float(0.58, iotype='in', desc='reference area')
    deaerationFlowLossCoef = Float(0.33, iotype='in', desc='electric pump actual run speed')
    doSandUpgrade = Float(1.0, iotype='in', desc='boolean to do retrofit or not')

    # lighting model
    numBulbs = Float(1.0, iotype='in', desc='number of bulbs to replace')

    # set up outputs
    # potential constraints
    proteinHead = Float(25.0, iotype='out', desc='simulated head')
    totalFlowSand = Float(63000.0, iotype='out', desc='total gallons per minute sand filters')
    totalFlowProtein = Float(55358.0, iotype='out', desc='total gallons per minute protein skimmers')
    heatExchFlow1 = Float(1000.0, iotype='out', desc='simulated head')
    heatExchFlow2 = Float(1000.0, iotype='out', desc='simulated head')
    denitFlow = Float(8000.0, iotype='out', desc='simulated head')
    bypassFlow = Float(45500.0, iotype='out', desc='simulated head')
    ozFlow = Float(600.0, iotype='out', desc='ozone path towers 1-6 flow')
    sandFilterFlow = Float(800.0, iotype='out', desc='flow through one of the sand filters')

    # power
    proteinPumpPower = Float(10.0, iotype='out', desc='power in kW for protein skimmer pump')
    sandPumpPower = Float(10.0, iotype='out', desc='power in kW for sand filter pump')
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
                      self.flowLossCoef, self.heatExchFlowLossCoef, self.heatExchValveOpen, self.denitFlowLossCoef,
                      self.ozoneFlowLossCoef, self.ozoneValveOpen, self.denitValveOpen, self.deaerationFlowLossCoef]

        # Calculations for protein skimmers
        # This calculation is dependent on whether or not we'd like to do an upgrade. The upgrade is essentially the
        # controlling design variable, while the actual hydraulic-specific variables are only relevant if we perform
        # the upgrade. Otherwise, we set the output values to their default.
        if self.doProteinUpgrade == 1.0:
            # Calculate protein performance attributes
            self.totalPowerProtein, \
            self.proteinHead, \
            self.totalFlowProtein, \
            self.proteinPumpPower = calc_protein_power(self.protein_surrogate, inputsProtein, self.numProteinPumps)

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
            self.proteinPumpPower = self.currentProteinPumpKw / self.numProteinPumps

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
            self.totalFlowSand,\
            self.sandPumpPower,\
            self.ozFlow = calc_sand_power(self.sand_surrogate, inputsSand, self.numSandPumps)

            # Calculate sand filter cost
            self.sandCapitalCost = calc_sand_cost(self.numSandPumps, self.pumpModificationUnitCost,
                                                  self.pumpRatedRpm, self.currentSandRatedSpeed,
                                                  self.pumpFlow, self.currentSandRatedFlow,
                                                  self.pumpEff, self.currentSandRatedEff,
                                                  self.pumpRatedHead, self.currentSandRatedHead,
                                                  self.flowLossCoef, self.currentSandCircuitLoss,
                                                  self.heatExchFlowLossCoef, self.currentSandHxCircuitLoss,
                                                  self.ozoneFlowLossCoef, self.currentSandOzCircuitLoss,
                                                  self.denitFlowLossCoef, self.currentSandDnCircuitLoss,
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


class OceanVoyagerOptimization(Assembly):
    '''
    Implements an assembly to contain the SolarModel component, and run optimizations on it stand-alone with the
    pyOpt plugin of optimization drivers. Implements a caserecorder so that you can investigate the results
    afterwards. This assembly will show up automatically when using openmdao gui, or can be used directly in another
    python script as you would use a regular python class.
    '''

    def configure(self):
        '''
        This method is used to implement the custom behavior of the SolarOptimization Assembly. OpenMDAO requires
        that you implement this method, and it is used to add the optimization component, the SolarModel,
        and to configure the parameters within the optimization component.

        :returns: Outputs optimization results to the console and saves all data for inputs and outputs into a CSV \
        file named 'solar_optimization.csv'.

        '''

        # Add the pyOpt driver and case recorder
        self.replace("driver", pyOptDriver())
        self.driver.recorders.append(CSVCaseRecorder(filename='oceanvoyager_optimization.csv'))
        self.driver.optimizer = 'ALPSO'
        #self.driver.options['SwarmSize'] = 100

        # Add the solar model to the assembly
        self.add("ovm", OceanVoyagerModel())

        # Add the parameters to be used in optimization
        # OceanVoyager protein skimmers
        #self.driver.add_parameter('ovm.proteinRatedSpeed', low=800.0, high=1600.0)
        #self.driver.add_parameter('ovm.ratedHead', low=20.0, high=40.0)
        #self.driver.add_parameter('ovm.ratedFlow', low=1300.0, high=2000.0)
        #self.driver.add_parameter('ovm.proteinRatedEff', low=0.6, high=0.9)
        #self.driver.add_parameter('ovm.runSpeed', low=800.0, high=1600.0)
        #self.driver.add_parameter('ovm.lossMultiplier', low=135.0, high=150.0)
        #self.driver.add_parameter('ovm.referenceArea', low=0.1, high=0.5)

        # OceanVoyager sand filters
        self.driver.add_parameter('ovm.pumpFlow', low=1300.0, high=1700.0)
        #self.driver.add_parameter('ovm.pumpEff', low=.78, high=.80)
        self.driver.add_parameter('ovm.pumpRatedHead', low=30.0, high=90.0)
        #self.driver.add_parameter('ovm.pumpRatedRpm', low=1000.0, high=1300.0)
        #self.driver.add_parameter('ovm.pumpRunRpm', low=1000.0, high=1300.0)
        #self.driver.add_parameter('ovm.flowLossCoef', low=0.1, high=10.0)
        #self.driver.add_parameter('ovm.heatExchFlowLossCoef', low=0.1, high=6.0)
        self.driver.add_parameter('ovm.heatExchValveOpen', low=0.01, high=1.0)
        #self.driver.add_parameter('ovm.denitFlowLossCoef', low=0.1, high=3.0)
        self.driver.add_parameter('ovm.denitValveOpen', low=0.01, high=1.0)
        #self.driver.add_parameter('ovm.ozoneFlowLossCoef', low=0.1, high=6.0)
        self.driver.add_parameter('ovm.ozoneValveOpen', low=0.01, high=1.0)
        #self.driver.add_parameter('ovm.deaerationFlowLossCoef', low=0.1, high=2.0)

        self.driver.add_objective('ovm.sandPumpPower')
        #self.driver.add_constraint('ovm.totalFlowProtein - 66000 < 0')
        #self.driver.add_constraint('ovm.totalFlowProtein - 60000 > 0')
        #self.driver.add_constraint('ovm.proteinPumpPower - 20 < 0')
        #self.driver.add_constraint('ovm.proteinPumpPower > 0')
        #self.driver.add_constraint('ovm.totalFlowSand - 61000 < 0')
        #self.driver.add_constraint('ovm.totalFlowSand -60000 > 0')
        #self.driver.add_constraint('ovm.sandFilterFlow - 800 < 0')
        #self.driver.add_constraint('ovm.sandFilterFlow > 0')
        # self.driver.add_constraint('ovm.heatExchFlow2 - 3500 < 0')
        # self.driver.add_constraint('ovm.heatExchFlow2 - 3000 > 0')
        # self.driver.add_constraint('ovm.denitFlow - 8500 < 0')
        # self.driver.add_constraint('ovm.denitFlow - 8000 > 0')
        # self.driver.add_constraint('ovm.bypassFlow - 43000 < 0')
        # self.driver.add_constraint('ovm.bypassFlow - 40000 > 0')
        # self.driver.add_constraint('ovm.ozFlow - 8500 < 0')
        # self.driver.add_constraint('ovm.ozFlow - 8000 > 0')
        self.driver.add_constraint('(ovm.heatExchFlow2 - 3250)/250 < 1')
        self.driver.add_constraint('(ovm.heatExchFlow2 - 3250)/250 > -1')
        self.driver.add_constraint('(ovm.denitFlow - 8250)/250 < 1')
        self.driver.add_constraint('(ovm.denitFlow - 8250)/250 > -1')
        self.driver.add_constraint('(ovm.bypassFlow - 41500)/1500 < 1')
        self.driver.add_constraint('(ovm.bypassFlow - 41500)/1500 > -1')
        self.driver.add_constraint('(ovm.ozFlow - 8250)/250 < 1')
        self.driver.add_constraint('(ovm.ozFlow - 8250)/250 > -1')

        self.driver.printvars =['ovm.totalFlowSand', 'ovm.sandFilterFlow', 'ovm.denitFlow', 'ovm.bypassFlow',
                                'ovm.heatExchFlow2', 'ovm.ozFlow', 'ovm.sandPumpPower']

class OceanVoyagerDoe(Assembly):
    '''
    An assembly to connect the optimizer directly to the Georgia Aquarium model. This can be used to avoid issues
    with the uncertainty distributions. After it is found that this assembly is working correctly, the next step
    would be to
    '''
    def configure(self):

        # Add components
        self.add('ovm', OceanVoyagerModel())
        self.replace("driver", DOEdriver())
        self.driver.recorders.append(CSVCaseRecorder(filename='ovm_simpledoe.csv'))

        # Add all components to the workflow
        self.driver.workflow.add("ovm", check=True)

        self.driver.add_parameter('ovm.pumpFlow', low=1300.0, high=1700.0)
        self.driver.add_parameter('ovm.pumpEff', low=.78, high=.8)
        self.driver.add_parameter('ovm.pumpRatedHead', low=40.0, high=80.0)
        self.driver.add_parameter('ovm.heatExchValveOpen', low=0.1, high=1.0)
        self.driver.add_parameter('ovm.denitValveOpen', low=0.1, high=1.0)
        self.driver.add_parameter('ovm.ozoneValveOpen', low=0.1, high=1.0)

        self.driver.add_objective('ovm.sandPumpPower')

        self.driver.printvars = ['ovm.totalInitialInvestment', 'ovm.breakEvenYear', 'ovm.totalFlowProtein',
                                 'ovm.year5Roi', 'ovm.originalEnergyCost', 'ovm.totalEnergyCost', 'ovm.totalEnergySaved',
                                 'ovm.totalPowerConsumed', 'ovm.totalPowerProduced', 'ovm.baselineOceanVoyPowerUse',
                                 'ovm.baselineTotalPowerUse', 'ovm.totalPowerProtein', 'ovm.totalPowerSand',
                                 'ovm.sandPumpPower']

        self.driver.add("DOEgenerator", LatinHypercube(num_samples=10000))


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    from test_ocean_voyager import test_ov_openmdao_model, test_ov_openmdao_optimization
    test_ov_openmdao_model()
    test_ov_openmdao_optimization()