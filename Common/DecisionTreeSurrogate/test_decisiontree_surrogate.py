__author__ = 'Nick'

from create_decision_tree import init_surrogate
def test_decision_tree():
    surr = init_surrogate()
    print surr.sim([[500.0]])