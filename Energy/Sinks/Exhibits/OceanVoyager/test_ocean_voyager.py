__author__ = 'Nick'

from OceanVoyager import OceanVoyagerModel
from Common.AttributeTools.io import print_outputs
from OceanVoyager import OceanVoyagerOptimization, OceanVoyagerDoe


def test_ov_openmdao_model():
    # Module test routine, only executes when this python is ran independently
    # For example, using Pycharm, right click while editing and select Run
    comp = OceanVoyagerModel()
    comp.execute()
    print_outputs(comp)


def test_ov_openmdao_optimization():
    ovo = OceanVoyagerOptimization()
    ovo.run()

def test_ov_openmdao_doe():
    ovd = OceanVoyagerDoe()
    ovd.execute()