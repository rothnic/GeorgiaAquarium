__author__ = 'Nick'

from openmdao.main.api import Assembly
from openmdao.lib.casehandlers.api import CSVCaseRecorder
from pyopt_driver.pyopt_driver import pyOptDriver
from openmdao.lib.drivers.doedriver import DOEdriver
#from openmdao.lib.drivers.api import CONMINdriver
from openmdao.lib.doegenerators.optlh import LatinHypercube
from Uncertainties.Uncertainties import UncertaintiesModel
from Common.RunAggregator.RunAggregator import RunAggregator
from openmdao.lib.drivers.genetic import Genetic
import os
import GeorgiaAquarium as ga

class GeorgiaAquariumGlobalOptimization(Assembly):
    def configure(self):
        # Create wrapper for sampler so we only see the final averaged output from the LHS runs
        self.add('gas', GeorgiaAquariumSampler())
        self.driver.workflow.add('gas', check=True)

        # Create passthroughs to optimizer
        self.create_passthrough('gas.bladeLength')
        self.create_passthrough('gas.proteinRatedEff')
        self.create_passthrough('gas.ratedFlow')
        self.create_passthrough('gas.proteinHead')
        self.create_passthrough('gas.proteinRatedSpeed')
        self.create_passthrough('gas.referenceArea')
        self.create_passthrough('gas.runSpeed')
        self.create_passthrough('gas.surfaceArea')
        self.create_passthrough('gas.tileCount')
        self.create_passthrough('gas.turbineCount')
        self.create_passthrough('gas.breakEvenYearMean')
        self.create_passthrough('gas.proteinHeadMean')
        self.create_passthrough('gas.originalEnergyCostMean')
        self.create_passthrough('gas.totalEnergyCostMean')
        self.create_passthrough('gas.totalEnergySavedMean')
        self.create_passthrough('gas.totalFlowProteinMean')
        self.create_passthrough('gas.totalInitialInvestmentMean')
        self.create_passthrough('gas.totalPowerConsumedMean')
        self.create_passthrough('gas.totalPowerProducedMean')
        self.create_passthrough('gas.totalUtilityMean')
        self.create_passthrough('gas.year10RoiMean')
        self.create_passthrough('gas.year1RoiMean')
        self.create_passthrough('gas.year20RoiMean')
        self.create_passthrough('gas.year30RoiMean')
        self.create_passthrough('gas.year5RoiMean')


class GeorgiaAquariumSampler(Assembly):
    def configure(self):
        # Add components
        self.add('um', UncertaintiesModel())
        self.add('ga', ga.GeorgiaAquarium())
        self.add('ra', RunAggregator())

        # Add all components to the workflow
        self.replace("driver", DOEdriver())
        self.driver.workflow.add("um", check=True)
        self.driver.workflow.add("ga", check=True)
        self.driver.workflow.add("ra", check=True)

        # Make internal connections
        self.connect("um.pedsPerHourOff", "ga.pedsPerHourOff")
        self.connect("um.pedsPerHourOn", "ga.pedsPerHourOn")
        self.connect("ga.breakEvenYear", "ra.breakEvenYearSamp")
        self.connect("ga.proteinHead", "ra.proteinHeadSamp")
        self.connect("ga.originalEnergyCost", "ra.originalEnergyCostSamp")
        self.connect("ga.totalEnergyCost", "ra.totalEnergyCostSamp")
        self.connect("ga.totalEnergySaved", "ra.totalEnergySavedSamp")
        self.connect("ga.totalFlowProtein", "ra.totalFlowProteinSamp")
        self.connect("ga.totalInitialInvestment", "ra.totalInitialInvestmentSamp")
        self.connect("ga.totalPowerConsumed", "ra.totalPowerConsumedSamp")
        self.connect("ga.totalPowerProduced", "ra.totalPowerProducedSamp")
        self.connect("ga.totalUtility", "ra.totalUtilitySamp")
        self.connect("ga.year10Roi", "ra.year10RoiSamp")
        self.connect("ga.year1Roi", "ra.year1RoiSamp")
        self.connect("ga.year20Roi", "ra.year20RoiSamp")
        self.connect("ga.year30Roi", "ra.year30RoiSamp")
        self.connect("ga.year5Roi", "ra.year5RoiSamp")

        # Replace with LHS
        self.driver.add("DOEgenerator", LatinHypercube(num_samples=50))

        # Add parameters to Driver
        # Uncertainty variables are sampled as invest CDFs, so should always be low=0, high=1
        self.driver.add_parameter('um.pedsPerHourOff_prob', low=0, high=1)
        self.driver.add_parameter('um.pedsPerHourOn_prob', low=0, high=1)

        # Setup passthroughs for design variables and expected output values
        self.create_passthrough('ga.bladeLength')
        self.create_passthrough('ga.proteinRatedSpeed')
        self.create_passthrough('ga.proteinHead')
        self.create_passthrough('ga.ratedFlow')
        self.create_passthrough('ga.surfaceArea')
        self.create_passthrough('ga.tileCount')
        self.create_passthrough('ga.turbineCount')
        self.create_passthrough('ga.runSpeed')
        self.create_passthrough('ga.referenceArea')
        self.create_passthrough('ga.proteinRatedEff')
        self.create_passthrough('ra.breakEvenYearMean')
        self.create_passthrough('ra.proteinHeadMean')
        self.create_passthrough('ra.originalEnergyCostMean')
        self.create_passthrough('ra.totalEnergyCostMean')
        self.create_passthrough('ra.totalEnergySavedMean')
        self.create_passthrough('ra.totalFlowProteinMean')
        self.create_passthrough('ra.totalInitialInvestmentMean')
        self.create_passthrough('ra.totalPowerConsumedMean')
        self.create_passthrough('ra.totalPowerProducedMean')
        self.create_passthrough('ra.totalUtilityMean')
        self.create_passthrough('ra.year10RoiMean')
        self.create_passthrough('ra.year1RoiMean')
        self.create_passthrough('ra.year20RoiMean')
        self.create_passthrough('ra.year30RoiMean')
        self.create_passthrough('ra.year5RoiMean')


class GeorgiaAquariumOptimization(Assembly):
    '''
    An assembly to connect the optimizer directly to the Georgia Aquarium model. This can be used to avoid issues
    with the uncertainty distributions. After it is found that this assembly is working correctly, the next step
    would be to
    '''

    def __init__(self, breakEven=3.0, initialInvestment=400000.0, filename=''):
        self.breakEven = breakEven
        self.initialInvestment = initialInvestment
        self.initialInvestmentStr = 'ga.totalInitialInvestment - ' + str(self.initialInvestment) + ' < 0.0'
        self.breakEvenStr = 'ga.breakEvenYear - ' + str(self.breakEven) + ' < 0.0'
        self.filename = 'ga_simpleoptimization_' + str(filename) + '.csv'
        super(GeorgiaAquariumOptimization, self).__init__()

    def configure(self):
        path = os.path.dirname(os.path.realpath(__file__))

        # Add components
        self.add('ga', ga.GeorgiaAquarium())
        self.replace("driver", pyOptDriver())
        self.driver.recorders.append(CSVCaseRecorder(filename=self.filename))
        self.driver.optimizer = 'ALPSO'
        #self.driver.pyopt_diff = True

        # Add all components to the workflow
        self.driver.workflow.add("ga", check=True)

        # Add parameters to Optimization Driver
        # OceanVoyager protein skimmers
        self.driver.add_parameter('ga.bladeLength', low=1.5, high=2.5)

        # OceanVoyager Lighting
        self.driver.add_parameter('ga.numBulbs', low=0.0, high=40.0)

        # Kinetic
        self.driver.add_parameter('ga.tileCount', low=0.0, high=100.0)

        # Wind
        self.driver.add_parameter('ga.turbineCount', low=0.0, high=25.0)

        # Solar
        self.driver.add_parameter('ga.panelEff', low=.05, high=.25)
        self.driver.add_parameter('ga.panelRating', low=100, high=450)
        self.driver.add_parameter('ga.surfaceArea', low=0.0, high=1000.0)

        # Define Objective
        self.driver.add_objective('-ga.year5Roi')

        # Define Constraints
        self.driver.add_constraint(self.initialInvestmentStr)
        self.driver.add_constraint(self.breakEvenStr)


        # Configure additional logged variables
        self.driver.printvars = ['ga.totalInitialInvestment', 'ga.breakEvenYear', 'ga.totalFlowProtein',
                                 'ga.year5Roi', 'ga.originalEnergyCost', 'ga.totalEnergyCost', 'ga.totalEnergySaved',
                                 'ga.totalPowerConsumed', 'ga.totalPowerProduced', 'ga.baselineOceanVoyPowerUse',
                                 'ga.baselineTotalPowerUse', 'ga.totalPowerProtein', 'ga.totalPowerSand']

class GeorgiaAquariumDoe(Assembly):
    '''
    An assembly to connect the optimizer directly to the Georgia Aquarium model. This can be used to avoid issues
    with the uncertainty distributions. After it is found that this assembly is working correctly, the next step
    would be to
    '''
    def configure(self):
        path = os.path.dirname(os.path.realpath(__file__))

        # Add components
        self.add('ga', ga.GeorgiaAquarium())
        self.replace("driver", DOEdriver())
        self.driver.recorders.append(CSVCaseRecorder(filename='ga_simpledoe.csv'))

        # Add all components to the workflow
        self.driver.workflow.add("ga", check=True)

        # Add parameters to Optimization Driver
        # OceanVoyager protein skimmers
        self.driver.add_parameter('ga.bladeLength', low=1.5, high=2.5)
        #self.driver.add_parameter('ga.proteinRatedSpeed', low=800.0, high=1600.0)
        #self.driver.add_parameter('ga.ratedHead', low=20.0, high=40.0)
        #self.driver.add_parameter('ga.ratedFlow', low=1300.0, high=2000.0)
        #self.driver.add_parameter('ga.proteinRatedEff', low=0.6, high=0.9)
        #self.driver.add_parameter('ga.runSpeed', low=800.0, high=1600.0)
        #self.driver.add_parameter('ga.lossMultiplier', low=135.0, high=150.0)
        #self.driver.add_parameter('ga.referenceArea', low=0.1, high=0.5)

        # OceanVoyager sand filters
        # self.driver.add_parameter('ga.pumpFlow', low=1300.0, high=1700.0)
        # self.driver.add_parameter('ga.pumpEff', low=.6, high=.9)
        # self.driver.add_parameter('ga.pumpRatedHead', low=40.0, high=80.0)
        # self.driver.add_parameter('ga.pumpRatedRpm', low=1000.0, high=1300.0)
        # self.driver.add_parameter('ga.pumpRunRpm', low=1000.0, high=1300.0)
        # self.driver.add_parameter('ga.flowLossCoef', low=0.1, high=10.0)
        # self.driver.add_parameter('ga.heatExchFlowLossCoef', low=0.1, high=6.0)
        # self.driver.add_parameter('ga.heatExchValveOpen', low=0.1, high=1.0)
        # self.driver.add_parameter('ga.denitFlowLossCoef', low=0.1, high=3.0)
        # self.driver.add_parameter('ga.denitValveOpen', low=0.1, high=1.0)
        # self.driver.add_parameter('ga.ozoneFlowLossCoef', low=0.1, high=6.0)
        # self.driver.add_parameter('ga.ozoneValveOpen', low=0.1, high=1.0)
        # self.driver.add_parameter('ga.deaerationFlowLossCoef', low=0.1, high=2.0)

        # OceanVoyager Lighting
        self.driver.add_parameter('ga.numBulbs', low=0.0, high=40.0)

        self.driver.add_parameter('ga.tileCount', low=0.0, high=100.0)
        self.driver.add_parameter('ga.turbineCount', low=0.0, high=25.0)

        self.driver.add_parameter('ga.panelEff', low=.05, high=.25)
        self.driver.add_parameter('ga.panelRating', low=100, high=450)
        self.driver.add_parameter('ga.surfaceArea', low=0.0, high=1000.0)
        self.driver.printvars = ['ga.totalInitialInvestment', 'ga.breakEvenYear', 'ga.totalFlowProtein',
                                 'ga.year5Roi', 'ga.originalEnergyCost', 'ga.totalEnergyCost', 'ga.totalEnergySaved',
                                 'ga.totalPowerConsumed', 'ga.totalPowerProduced', 'ga.baselineOceanVoyPowerUse',
                                 'ga.baselineTotalPowerUse', 'ga.totalPowerProtein', 'ga.totalPowerSand',
                                 'ga.year1Roi', 'ga.year10Roi', 'ga.year20Roi', 'ga.year30Roi']
        self.driver.add("DOEgenerator", LatinHypercube(num_samples=10000))



if __name__=="__main__":
    #gao = GeorgiaAquariumOptimization()
    #gao.execute()
    gad = GeorgiaAquariumDoe()
    gad.execute()
