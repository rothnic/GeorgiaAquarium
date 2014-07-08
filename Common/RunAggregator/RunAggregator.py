__author__ = 'Nick'

from openmdao.main.api import Assembly, Component
from openmdao.lib.drivers import doedriver
from openmdao.lib.datatypes.api import Float
from Common.AttributeTools.io import get_output_values, get_inputs, get_outputs, get_input_values, print_outputs
import numpy as np

class RunAggregator(Component):

    # set up inputs
    breakEvenYearSamp = Float(500.0, iotype='in', desc='break even year sample')
    headOutSamp = Float(500.0, iotype='in', desc='head out sample')
    originalEnergyCostSamp = Float(500.0, iotype='in', desc='original/baseline energy cost sample')
    totalEnergyCostSamp = Float(500.0, iotype='in', desc='total energy cost sample')
    totalEnergySavedSamp = Float(500.0, iotype='in', desc='total energy saved sample')
    totalFlowSamp = Float(500.0, iotype='in', desc='total flow sample')
    totalInitialInvestmentSamp = Float(500.0, iotype='in', desc='total initial investment sample')
    totalPowerConsumedSamp = Float(500.0, iotype='in', desc='total power consumed sample')
    totalPowerProducedSamp = Float(500.0, iotype='in', desc='total power produced sample')
    totalUtilitySamp = Float(500.0, iotype='in', desc='total utility sample')
    year1RoiSamp = Float(500.0, iotype='in', desc='year 1 ROI sample')
    year5RoiSamp = Float(500.0, iotype='in', desc='year 5 ROI sample')
    year10RoiSamp = Float(500.0, iotype='in', desc='year 10 ROI sample')
    year20RoiSamp = Float(500.0, iotype='in', desc='year 20 ROI sample')
    year30RoiSamp = Float(500.0, iotype='in', desc='year 30 ROI sample')

    # set up outputs
    breakEvenYearMean = Float(500.0, iotype='out', desc='break even year mean')
    headOutMean = Float(500.0, iotype='out', desc='head out mean')
    originalEnergyCostMean = Float(500.0, iotype='out', desc='original/baseline energy cost mean')
    totalEnergyCostMean = Float(500.0, iotype='out', desc='total energy cost mean')
    totalEnergySavedMean = Float(500.0, iotype='out', desc='total energy saved mean')
    totalFlowMean = Float(500.0, iotype='out', desc='total flow mean')
    totalInitialInvestmentMean = Float(500.0, iotype='out', desc='total initial investment mean')
    totalPowerConsumedMean = Float(500.0, iotype='out', desc='total power consumed mean')
    totalPowerProducedMean = Float(500.0, iotype='out', desc='total power produced mean')
    totalUtilityMean = Float(500.0, iotype='out', desc='total utility mean')
    year1RoiMean = Float(500.0, iotype='out', desc='year 1 ROI mean')
    year5RoiMean = Float(500.0, iotype='out', desc='year 5 ROI mean')
    year10RoiMean = Float(500.0, iotype='out', desc='year 10 ROI mean')
    year20RoiMean = Float(500.0, iotype='out', desc='year 20 ROI mean')
    year30RoiMean = Float(500.0, iotype='out', desc='year 30 ROI mean')

    exec_num = 0.0

    #Todo improve the speed by not using python dicts
    def __init__(self):
        super(RunAggregator, self).__init__()
        self.output_names = get_outputs(self)

        self.outputs = {}
        for output_name in self.output_names:
            self.outputs[output_name] = np.array([])


    def execute(self):

        # Get the values from last run
        self.inputs = get_input_values(self)

        # Calculate the mean value of all input values so far
        for input, output in zip(self.inputs, self.outputs):
            self.outputs[output] = np.append(self.outputs[output], self.inputs[input])
            if self.exec_num >= 1.0:
                setattr(self, output, np.mean(self.outputs[output]))

        self.exec_num += 1.0


def run_tests():
    import random as rand

    agg = RunAggregator()
    inputs = get_inputs(agg)
    for count in xrange(1, 10, 1):
        for input in inputs:
            setattr(agg, input, np.float(rand.randrange(20, 200)))
        agg.execute()
        print_outputs(agg)

if __name__=="__main__":
    run_tests()