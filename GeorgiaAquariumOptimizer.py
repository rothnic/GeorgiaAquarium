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
        self.create_passthrough('gas.ratedEff')
        self.create_passthrough('gas.ratedFlow')
        self.create_passthrough('gas.ratedHead')
        self.create_passthrough('gas.ratedSpeed')
        self.create_passthrough('gas.referenceArea')
        self.create_passthrough('gas.runSpeed')
        self.create_passthrough('gas.surfaceArea')
        self.create_passthrough('gas.tileCount')
        self.create_passthrough('gas.turbineCount')
        self.create_passthrough('gas.breakEvenYearMean')
        self.create_passthrough('gas.headOutMean')
        self.create_passthrough('gas.originalEnergyCostMean')
        self.create_passthrough('gas.totalEnergyCostMean')
        self.create_passthrough('gas.totalEnergySavedMean')
        self.create_passthrough('gas.totalFlowMean')
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

        # Make connections between internal components
        self.connect("um.pedsPerHourOff", "ga.pedsPerHourOff")
        self.connect("um.pedsPerHourOn", "ga.pedsPerHourOn")
        self.connect("ga.breakEvenYear", "ra.breakEvenYearSamp")
        self.connect("ga.proteinHead", "ra.headOutSamp")
        self.connect("ga.originalEnergyCost", "ra.originalEnergyCostSamp")
        self.connect("ga.totalEnergyCost", "ra.totalEnergyCostSamp")
        self.connect("ga.totalEnergySaved", "ra.totalEnergySavedSamp")
        self.connect("ga.totalProteinFlow", "ra.totalProteinFlowSamp")
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
        self.create_passthrough('ga.ratedSpeed')
        self.create_passthrough('ga.proteinHead')
        self.create_passthrough('ga.ratedFlow')
        self.create_passthrough('ga.surfaceArea')
        self.create_passthrough('ga.tileCount')
        self.create_passthrough('ga.turbineCount')
        self.create_passthrough('ga.runSpeed')
        self.create_passthrough('ga.referenceArea')
        self.create_passthrough('ovm.proteinRatedEff')
        self.create_passthrough('ra.breakEvenYearMean')
        self.create_passthrough('ra.headOutMean')
        self.create_passthrough('ra.originalEnergyCostMean')
        self.create_passthrough('ra.totalEnergyCostMean')
        self.create_passthrough('ra.totalEnergySavedMean')
        self.create_passthrough('ra.totalFlowMean')
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
    def configure(self):
        path = os.path.dirname(os.path.realpath(__file__))

        # Add components
        self.add('ga', ga.GeorgiaAquarium())
        self.replace("driver", pyOptDriver())
        self.driver.recorders.append(CSVCaseRecorder(filename='ga_simpleoptimization.csv'))

        # Add all components to the workflow
        self.driver.workflow.add("ga", check=True)

        # Add parameters to Optimization Driver
        self.driver.add_parameter('ga.bladeLength', low=0.0, high=5.0)
        self.driver.add_parameter('ga.proteinRatedSpeed', low=100.0, high=1500.0)
        self.driver.add_parameter('ga.ratedHead', low=20.0, high=40.0)
        self.driver.add_parameter('ga.ratedFlow', low=1300.0, high=2000.0)
        self.driver.add_parameter('ga.tileCount', low=0.0, high=100.0)
        self.driver.add_parameter('ga.turbineCount', low=0.0, high=25.0)
        self.driver.add_parameter('ga.runSpeed', low=800.0, high=1600.0)
        self.driver.add_parameter('ga.referenceArea', low=.1, high=.5)
        self.driver.add_parameter('ga.pumpEff', low=.6, high=.9)
        self.driver.add_parameter('ga.panelEff', low=.05, high=.25)
        self.driver.add_parameter('ga.panelRating', low=100, high=450)
        self.driver.add_parameter('ga.surfaceArea', low=0.0, high=1000.0)
        self.driver.add_objective('-ga.year5Roi')
        self.driver.add_constraint('ga.totalInitialInvestment-400000.0 <= 0.0')
        self.driver.add_constraint('ga.breakEvenYear - 3.0 < 0')
        self.driver.add_constraint('ga.totalFlowProtein-66000 < 0')
        self.driver.add_constraint('ga.totalFlowProtein-60000 > 0')
        self.driver.printvars = ['ga.totalInitialInvestment', 'ga.breakEvenYear', 'ga.totalFlowProtein', 'ga.year5Roi']

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
        #self.driver.add_parameter('ga.doProteinUpgrade', low=0.0, high=1.0)
        #self.driver.add_parameter('ga.doSandUpgrade', low=0.0, high=1.0)
        self.driver.add_parameter('ga.bladeLength', low=1.0, high=5.0)
        self.driver.add_parameter('ga.proteinRatedSpeed', low=100.0, high=1500.0)
        self.driver.add_parameter('ga.ratedHead', low=20.0, high=40.0)
        self.driver.add_parameter('ga.ratedFlow', low=1300.0, high=2000.0)
        self.driver.add_parameter('ga.tileCount', low=1.0, high=100.0)
        self.driver.add_parameter('ga.turbineCount', low=1.0, high=25.0)
        self.driver.add_parameter('ga.runSpeed', low=800.0, high=1600.0)
        self.driver.add_parameter('ga.referenceArea', low=.1, high=.5)
        self.driver.add_parameter('ga.pumpEff', low=.6, high=.9)
        self.driver.add_parameter('ga.panelEff', low=.05, high=.25)
        self.driver.add_parameter('ga.panelRating', low=100, high=450)
        self.driver.add_parameter('ga.surfaceArea', low=0, high=1000)
        self.driver.case_outputs = ['ga.totalInitialInvestment', 'ga.breakEvenYear', 'ga.totalFlowProtein',
                                    'ga.year5Roi', 'ga.solarCapitalCost', 'ga.triboCapitalCost', 'ga.windCapitalCost',
                                    'ga.hydraulicCapitalCost']
        self.driver.add("DOEgenerator", LatinHypercube(num_samples=1000))



if __name__=="__main__":
    gao = GeorgiaAquariumOptimization()
    gao.execute()
    gad = GeorgiaAquariumDoe()
    gad.execute()
