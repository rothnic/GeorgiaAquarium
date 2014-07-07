__author__ = 'Nick'

from calc_cost import *
from Cost import CostModel
from Common.AttributeTools.io import get_output_values

def test_roi():
    output = calc_roi(1000.0, 100000.0, 100001.0)
    assert sum(output) is not 0

def test_break_even():
    output = get_break_even(1000.0, 100000.0, 100001.0)
    assert output == 1000

def test_cost_component():
    cm = CostModel()
    cm.execute()
    outputs = get_output_values(cm)
    assert type(outputs) is dict