__author__ = 'Nick'

from OceanVoyager import OceanVoyagerModel
from Common.AttributeTools.io import print_outputs

def test_ov_openmdao_model():
    # Module test routine, only executes when this python is ran independently
    # For example, using Pycharm, right click while editing and select Run
    comp = OceanVoyagerModel()
    comp.execute()
    print_outputs(comp)