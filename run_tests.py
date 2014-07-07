__author__ = 'Nick'

from Uncertainties import Uncertainties
from Pedestrian import Pedestrian
from Energy.Sources.Solar import Solar
from Energy.Sources.Wind import Wind
from Energy.Sinks.Exhibits.OceanVoyager import OceanVoyager

Uncertainties.run_tests()
Pedestrian.run_tests()
Solar.run_tests()
Wind.run_tests()
OceanVoyager.run_tests()