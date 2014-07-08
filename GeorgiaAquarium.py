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

class GeorgiaAquarium(Assembly):

    def configure(self):

        self.add('cm', CostModel())
        self.add('tb', TriboModel())
        self.add('wm', WindModel())
        self.add('sm', SolarModel())
        self.add('ovm', OceanVoyagerModel())
        self.add('pm', PedestrianModel())

        #Add all components to the workflow
        self.driver.workflow.add("ovm", check=True)
        self.driver.workflow.add("tb", check=True)
        self.driver.workflow.add("sm", check=True)
        self.driver.workflow.add("wm", check=True)
        self.driver.workflow.add("cm", check=True)
        self.driver.workflow.add("pm", check=True)

        #Internal Connections
        self.connect("tb.totalkWh","cm.yearlyPowerProducedTribo")
        self.connect("tb.triboCapitalCost","cm.triboCapitalCost")
        self.connect("wm.totalkWh","cm.yearlyPowerProducedWind")
        self.connect("wm.windCapitalCost","cm.windCapitalCost")
        self.connect("sm.solarCapitalCost","cm.solarCapitalCost")
        self.connect("sm.totalkWh","cm.yearlyPowerProducedSolar")
        self.connect("ovm.hydraulicCapitalCost","cm.hydraulicCapitalCost")
        self.connect("ovm.totalPowerUsed","cm.hydraulicPowerUse")
        self.connect("pm.yearlyStepsPerTile","tb.pedStepsPerTile")

        #Passthrough Connections
        self.create_passthrough('cm.elecUtilityRate')
        self.create_passthrough('wm.airDensity')
        self.create_passthrough('cm.baselineOceanVoyPowerUse')
        self.create_passthrough('cm.baselineTotalPowerUse')
        self.create_passthrough('wm.bladeLength')
        self.create_passthrough('wm.circuitLoss')
        self.create_passthrough('wm.turbineCount')
        self.create_passthrough('wm.turbineEff')
        self.create_passthrough('wm.turbineRating')
        self.create_passthrough('wm.windCostPerWatt')
        self.create_passthrough('wm.windSpeedScalar')
        self.create_passthrough('sm.batteryCost')
        self.create_passthrough('sm.panelEff')
        self.create_passthrough('sm.panelRating')
        self.create_passthrough('sm.solarCostPerWatt')
        self.create_passthrough('sm.sunRadianceScalar')
        self.create_passthrough('sm.surfaceArea')
        self.create_passthrough('tb.mgtTileUnitCost')
        self.create_passthrough('tb.tileCount')
        self.create_passthrough('tb.tileEff')
        self.create_passthrough('tb.tileUnitCost')
        self.create_passthrough('tb.tilekWh')
        self.create_passthrough('ovm.lossMultiplier')
        self.create_passthrough('ovm.ratedEff')
        self.create_passthrough('ovm.ratedFlow')
        self.create_passthrough('ovm.ratedHead')
        self.create_passthrough('ovm.ratedSpeed')
        self.create_passthrough('ovm.referenceArea')
        self.create_passthrough('ovm.runSpeed')
        self.create_passthrough('cm.breakEvenYear')
        self.create_passthrough('cm.originalEnergyCost')
        self.create_passthrough('cm.totalEnergyCost')
        self.create_passthrough('cm.totalEnergySaved')
        self.create_passthrough('cm.totalInitialInvestment')
        self.create_passthrough('cm.totalPowerConsumed')
        self.create_passthrough('cm.totalPowerProduced')
        self.create_passthrough('cm.totalUtility')
        self.create_passthrough('cm.year10Roi')
        self.create_passthrough('cm.year1Roi')
        self.create_passthrough('cm.year20Roi')
        self.create_passthrough('cm.year30Roi')
        self.create_passthrough('cm.year5Roi')
        self.create_passthrough('ovm.headOut')
        self.create_passthrough('ovm.totalFlow')
        self.create_passthrough('pm.pedsPerHourOff')
        self.create_passthrough('pm.pedsPerHourOn')