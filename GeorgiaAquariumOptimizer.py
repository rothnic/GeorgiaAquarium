__author__ = 'Nick'

from openmdao.main.api import Assembly
from openmdao.main.driver import Driver
from openmdao.lib.doegenerators.api import FullFactorial
from openmdao.lib.casehandlers.api import ListCaseRecorder

from Cost.Cost import CostModel
from Pedestrian.Pedestrian import PedestrianModel
from Energy.Sinks.Exhibits.OceanVoyager.OceanVoyager import OceanVoyagerModel
from Energy.Sources.Solar.Solar import SolarModel
from Energy.Sources.Wind.Wind import WindModel
from Energy.Sources.Tribo.Tribo import TriboModel
from Uncertainties.Uncertainties import UncertaintiesModel
from Common.RunAggregator.RunAggregator import RunAggregator
from openmdao.lib.drivers.doedriver import DOEdriver
from openmdao.lib.doegenerators.optlh import OptLatinHypercube
import GeorgiaAquarium

class GeorgiaAquariumComponent(Assembly):

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
        self.add('ga', GeorgiaAquarium.GeorgiaAquarium())
        self.add('ra', RunAggregator())

        # Add all components to the workflow
        self.replace("driver", DOEdriver())
        self.driver.workflow.add("um", check=True)
        self.driver.workflow.add("ga", check=True)
        self.driver.workflow.add("ra", check=True)

        # Make connections between internal components
        self.connect("um.pedsPerHourOff","ga.pedsPerHourOff")
        self.connect("um.pedsPerHourOn","ga.pedsPerHourOn")
        self.connect("ga.breakEvenYear","ra.breakEvenYearSamp")
        self.connect("ga.headOut","ra.headOutSamp")
        self.connect("ga.originalEnergyCost","ra.originalEnergyCostSamp")
        self.connect("ga.totalEnergyCost","ra.totalEnergyCostSamp")
        self.connect("ga.totalEnergySaved","ra.totalEnergySavedSamp")
        self.connect("ga.totalFlow","ra.totalFlowSamp")
        self.connect("ga.totalInitialInvestment","ra.totalInitialInvestmentSamp")
        self.connect("ga.totalPowerConsumed","ra.totalPowerConsumedSamp")
        self.connect("ga.totalPowerProduced","ra.totalPowerProducedSamp")
        self.connect("ga.totalUtility","ra.totalUtilitySamp")
        self.connect("ga.year10Roi","ra.year10RoiSamp")
        self.connect("ga.year1Roi","ra.year1RoiSamp")
        self.connect("ga.year20Roi","ra.year20RoiSamp")
        self.connect("ga.year30Roi","ra.year30RoiSamp")
        self.connect("ga.year5Roi","ra.year5RoiSamp")

        # Replace with LHS
        self.driver.add("DOEgenerator", OptLatinHypercube(num_samples=50, population=10, generations=2))

        # Add parameters to Driver
        # Uncertainty variables are sampled as invest CDFs, so should always be low=0, high=1
        self.driver.add_parameter('um.pedsPerHourOff_prob',low=0,high=1)
        self.driver.add_parameter('um.pedsPerHourOn_prob',low=0,high=1)

        # Setup passthroughs for design variables and expected output values
        self.create_passthrough('ga.bladeLength')
        self.create_passthrough('ga.ratedSpeed')
        self.create_passthrough('ga.ratedHead')
        self.create_passthrough('ga.ratedFlow')
        self.create_passthrough('ga.surfaceArea')
        self.create_passthrough('ga.tileCount')
        self.create_passthrough('ga.turbineCount')
        self.create_passthrough('ga.runSpeed')
        self.create_passthrough('ga.referenceArea')
        self.create_passthrough('ga.ratedEff')
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
