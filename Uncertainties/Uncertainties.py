__author__ = 'Nick'

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from calc_uncertainties import Distribution
import pandas as pd

class UncertaintiesModel(Component):


    # set up inputs
    pedsPerHourOn_prob = Float(1.0, iotype='in', desc='avg peds per hour on season distribution sample point')
    pedsPerHourOff_prob = Float(1.0, iotype='in', desc='avg peds per hour off season distribution sample point')


    # set up outputs
    pedsPerHourOn = Float(1.0, iotype='out', desc='avg peds per hour on season distribution sample value')
    pedsPerHourOff = Float(1.0, iotype='out', desc='avg peds per hour off season distribution sample value')
    distributions = []

    def __init__(self):
        super(UncertaintiesModel, self).__init__()
        # set up constants
        path = os.path.dirname(os.path.realpath(__file__))
        self.filename = path + '\\uncertainties.csv'
        self.init_distributions(self.filename)

    def execute(self):
        # Loop through and sample all of my uncertainties
        for dist in self.distributions:
            # Get latest value from input probabilities
            probInput = getattr(self, dist.output + "_prob")
            setattr(self, dist.output, dist.sample(probInput))

    @property
    def my_outputs(self):
        my_outputs = self.list_outputs()
        standard_outputs = ['derivative_exec_count','exec_count','itername']
        my_outputs = list(set(my_outputs) - set(standard_outputs))
        return my_outputs

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
                        probData = table[col] # Probability series
                    else:
                        valueData = table[col] # Value series

            # Make sure we found the columns before creating distribution, otherwise raise error
            if isinstance(probData,pd.Series) and isinstance(valueData,pd.Series):
                self.distributions.append(Distribution(probData, valueData, output))
            else:
                raise NameError