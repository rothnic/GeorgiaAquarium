__author__ = 'Nick'

from Uncertainties import Uncertainties
from Energy.Sources.Solar import Solar
from Energy.Sources.Wind import Wind
from Energy.Sources.Tribo import Tribo
from Pedestrian import Pedestrian
from Cost import Cost
from Energy.Sinks.Exhibits.OceanVoyager import OceanVoyager
import GeorgiaAquarium as ga

Uncertainties.run_tests()
Solar.run_tests()
Wind.run_tests()
Tribo.run_tests()
Pedestrian.run_tests()
Cost.run_tests()
OceanVoyager.run_tests()
ga.run_tests()
