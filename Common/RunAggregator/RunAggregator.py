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
    totalFlowProteinSamp = Float(500.0, iotype='in', desc='total flow sample')
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
    totalFlowProteinwMean = Float(500.0, iotype='out', desc='total flow mean')
    totalInitialInvestmentMean = Float(500.0, iotype='out', desc='total initial investment mean')
    totalPowerConsumedMean = Float(500.0, iotype='out', desc='total power consumed mean')
    totalPowerProducedMean = Float(500.0, iotype='out', desc='total power produced mean')
    totalUtilityMean = Float(500.0, iotype='out', desc='total utility mean')
    year1RoiMean = Float(500.0, iotype='out', desc='year 1 ROI mean')
    year5RoiMean = Float(500.0, iotype='out', desc='year 5 ROI mean')
    year10RoiMean = Float(500.0, iotype='out', desc='year 10 ROI mean')
    year20RoiMean = Float(500.0, iotype='out', desc='year 20 ROI mean')
    year30RoiMean = Float(500.0, iotype='out', desc='year 30 ROI mean')

    # set up constants
    # None defined

    # initialization
    #Todo improve the speed by not using python dicts
    def __init__(self):
        '''
        Extend the OpenMDAO component init method only so that we can keep track of the execution state, collect the
        names of our configured outputs, and initialize the dict to store the samples over time.

        :return: Initialized OpenMDAO component object
        '''
        # ToDo: See if there is a way to turn this into a reusable component
        super(RunAggregator, self).__init__()
        self.exec_num = 0.0

        self.output_names = get_outputs(self)

        self.outputs = {}
        for output_name in self.output_names:
            self.outputs[output_name] = np.array([])

    # primary method
    def execute(self):
        '''
        The method that OpenMDAO requires that the behavior of the model be developed in. At each model execution,
        OpenMDAO will write new values into the components inputs, then will call this execute method. This component
        is different from the other model components because it exists simply to work with the Uncertainties model.
        The RunAggregator sit at a higher level than the GeorgiaAquarium assembly so that for each set of design
        variables, we can execute the GeorgiaAquarium model many times. During this time, the design variables do not
        change, but the uncertainties do change due to the sampling of them with a Latin Hypercube driver. We can
        execute the model like with without the RunAggregator, but the higher-level optimization component would only
        observe the last value.

        The RunAggregator observes all outputs from the samples associated with a single configuration of design
        variables and many samples across the uncertainties. For each output of the GeorgiaAquarium model,
        the RunAggregator stores the values in a python :class:`dict`, with a key equal to the name of the variable
        appended with "Mean", with a value of a :class:`~numpy.array` of length equal to the number of configured
        latin hypercube samples. Each time the RunAggregator is executed, the mean of the array is stored into the
        RunAggregator's output attributes.

        This component combined with the Uncertainties model replaces the functionality implemented in the Phoenix
        Integration ModelCenter Latin Hypercube driver combined with the cumulative distribution function excel
        spreadsheet, that has been used with it by Georgia Tech's PMASE program. Both of the components try to
        incorporate uncertainties into the model execution as a separate concept to design variables, allowing the
        model to converge to an expected value with enough runs.

        :returns: None
        '''

        # Get the values from last run
        self.inputs = get_input_values(self)

        # Calculate the mean value of all input values so far
        for input, output in zip(self.inputs, self.outputs):
            self.outputs[output] = np.append(self.outputs[output], self.inputs[input])
            if self.exec_num >= 1.0:
                setattr(self, output, np.mean(self.outputs[output]))

        self.exec_num += 1.0


if __name__=="__main__":
    '''
    A module testing routine, executes when this python file is ran independently. For example, using Pycharm,
    right click while editing and select Run. The tests called below are alternatively ran automatically by pytest
    from test_aggregator if configured to do so within Pycharm.
    '''
    from test_aggregator import test_meaning
    test_meaning()