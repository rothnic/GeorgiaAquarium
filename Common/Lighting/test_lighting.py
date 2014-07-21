__author__ = 'Nick'

from Lighting import LightingModel
from calc_lighting import Lights
from Common.AttributeTools.io import print_outputs

def setup_tests():
    lsOld = Lights([40], [1], [1000], [180], [10000], [12], [True])
    lsNew = Lights([30], [1.5], [120], [712], [50000], [12], [False])
    return lsOld, lsNew

def test_lights_initial():
    old, new = setup_tests()
    old.initial_cost
    new.initial_cost

def test_lights_power_year():
    old, new = setup_tests()
    old.power_per_year
    new.power_per_year

def test_lights_recurrance():
    old, new = setup_tests()
    old.recurrance_period
    new.recurrance_period

def test_lights_cost():
    old, new = setup_tests()
    old.recurring_cost
    new.recurring_cost

def test_lights_yearly_cost():
    old, new = setup_tests()
    old.yearly_cost()
    new.yearly_cost()

def test_lighting_model():
    old, new = setup_tests()
    lm = LightingModel(new, old)
    lm.execute()
    print_outputs(lm)