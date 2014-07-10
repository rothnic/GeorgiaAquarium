__author__ = 'Nick'

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_uncertainties import Distribution
from Common.AttributeTools.io import get_outputs, print_outputs


class UncertaintiesModel(Component):
    # set up inputs
    pedsPerHourOn_prob = Float(0.5, iotype='in', desc='avg peds per hour on season distribution sample point')
    pedsPerHourOff_prob = Float(0.5, iotype='in', desc='avg peds per hour off season distribution sample point')
    tileUnitCost_prob = Float(0.5, iotype='in', desc='cost of a tribo tile distribution sample point')
    elecUtilityRate_prob = Float(0.5, iotype='in', desc='cost of electricity distribution sample point')
    panelEff_prob = Float(0.5, iotype='in', desc='eff in conversion of sun energy distribution sample point')
    circuitLoss_prob = Float(0.5, iotype='in', desc='eff in collecting electrical energy distribution sample point')
    turbineEff_prob = Float(0.5, iotype='in', desc='eff in collecting electrical energy distribution sample point')
    baselineTotalPowerUse_prob = Float(0.5, iotype='in', desc='current power use per year distribution sample point')


    # set up outputs
    pedsPerHourOn = Float(600.0, iotype='out', desc='avg peds per hour on season distribution sample value')
    pedsPerHourOff = Float(500.0, iotype='out', desc='avg peds per hour off season distribution sample value')
    tileUnitCost = Float(800.0, iotype='out', desc='cost of a tribo tile distribution sample value')
    elecUtilityRate = Float(0.1, iotype='out', desc='cost of electricity distribution sample value')
    panelEff = Float(0.23, iotype='out', desc='eff in conversion of sun energy distribution sample value')
    circuitLoss = Float(0.30, iotype='out', desc='eff in collecting electrical energy distribution sample value')
    turbineEff = Float(0.367, iotype='out', desc='eff in collecting electrical energy distribution sample value')
    baselineTotalPowerUse = Float(1438775.0, iotype='out', desc='current power use per year distribution sample value')
    distributions = []

    def __init__(self):
        super(UncertaintiesModel, self).__init__()
        # set up constants
        path = os.path.dirname(os.path.realpath(__file__))
        self.my_outputs = get_outputs(self)
        self.filename = path + '\\uncertainties.csv'
        self.init_distributions(self.filename)

    def execute(self):
        # Loop through and sample all of my uncertainties
        for dist in self.distributions:
            # Get latest value from input probabilities
            probInput = getattr(self, dist.output + "_prob")
            setattr(self, dist.output, dist.sample(probInput))

    def init_distributions(self, filename):
        '''
        Inits probability and associated values from CSV
        :param output:
        :return:
        '''
        # Read in the CSV file
        table = pd.read_csv(filename)

        # Create distributions for each prob,value pair in the CSV file
        for output in self.my_outputs:
            probData, valueData = [], []
            for col in table.columns.values.tolist():
                if output in col:
                    if "prob" in col:
                        probData = table[col]  # Probability series
                    else:
                        valueData = table[col]  # Value series

            # Make sure we found the columns before creating distribution, otherwise raise error
            if isinstance(probData, pd.Series) and isinstance(valueData, pd.Series):
                self.distributions.append(Distribution(probData, valueData, output))
            else:
                raise NameError


def run_tests():
    # Module test routine, only executes when this python is ran independently
    # For example, using Pycharm, right click while editing and select Run
    comp = UncertaintiesModel()
    comp.execute()
    print_outputs(comp)


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()