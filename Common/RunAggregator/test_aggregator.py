__author__ = 'Nick'

from Common.RunAggregator.RunAggregator import RunAggregator
from Common.AttributeTools.io import print_outputs, get_inputs
import numpy as np


def test_meaning():
    import random as rand

    agg = RunAggregator()
    inputs = get_inputs(agg)
    for count in xrange(1, 10, 1):
        for input in inputs:
            setattr(agg, input, np.float(rand.randrange(20, 200)))
        agg.execute()
        print_outputs(agg)