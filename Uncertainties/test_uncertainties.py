__author__ = 'Nick'
from Uncertainties import UncertaintiesModel
from Common.AttributeTools.io import print_outputs

def test_uncertainties_component():
    # Module test routine, only executes when this python is ran independently
    # For example, using Pycharm, right click while editing and select Run
    comp = UncertaintiesModel()
    comp.execute()
    print_outputs(comp)