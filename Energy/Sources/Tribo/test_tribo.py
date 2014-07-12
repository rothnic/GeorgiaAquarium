__author__ = 'Nick'
from Tribo import TriboModel, TriboOptimization
from Common.AttributeTools.io import print_outputs

def test_tribo_openmdao_model():
    comp = TriboModel()
    comp.execute()
    print_outputs(comp)

def test_tribo_optimization():
    to = TriboOptimization()
    to.execute()