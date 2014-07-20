__author__ = 'Nick'

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd

from calc_uncertainties import Distribution
from Common.AttributeTools.io import get_outputs


class UncertaintiesModel(Component):
    # set up inputs
    pedsPerHourOn_prob = Float(0.5, iotype='in', desc='avg peds per hour on season distribution sample point')
    pedsPerHourOff_prob = Float(0.5, iotype='in', desc='avg peds per hour off season distribution sample point')
    tileUnitCost_prob = Float(0.5, iotype='in', desc='cost of a tribo tile distribution sample point')
    elecUtilityRate_prob = Float(0.5, iotype='in', desc='cost of electricity distribution sample point')
    panelEff_prob = Float(0.5, iotype='in', desc='eff in conversion of sun energy distribution sample point')
    circuitLoss_prob = Float(0.5, iotype='in', desc='eff in collecting electrical energy distribution sample point')
    turbineEff_prob = Float(0.5, iotype='in', desc='eff in collecting electrical energy distribution sample point')
    baselineOceanVoyPowerUse_prob = Float(0.5, iotype='in',desc='current power use per year for OV distribution sample point')
    baselineTotalPowerUse_prob = Float(0.5, iotype='in', desc='current power use per year for total aquarium '
                                                              'distribution sample point')

    # set up outputs
    pedsPerHourOn = Float(600.0, iotype='out', desc='avg peds per hour on season distribution sample value')
    pedsPerHourOff = Float(500.0, iotype='out', desc='avg peds per hour off season distribution sample value')
    tileUnitCost = Float(800.0, iotype='out', desc='cost of a tribo tile distribution sample value')
    elecUtilityRate = Float(0.1, iotype='out', desc='cost of electricity distribution sample value')
    panelEff = Float(0.23, iotype='out', desc='eff in conversion of sun energy distribution sample value')
    circuitLoss = Float(0.30, iotype='out', desc='eff in collecting electrical energy distribution sample value')
    turbineEff = Float(0.367, iotype='out', desc='eff in collecting electrical energy distribution sample value')
    baselineOceanVoyPowerUse = Float(17265306.1224, iotype='out', desc='current power use per year for OV '
                                                                       'distribution sample value')
    baselineTotalPowerUse = Float(27465306.1224, iotype='out', desc='current power use per year for total '
                                                                    'aquarium distribution sample value')

    # set up constants
    # None defined

    # initialization
    def __init__(self):
        '''
        The constructor of the OpenMDAO component is extended to initialize a :class:`list` to contain the
        distributions, then it loads the CSV file containing the uncertainties data, then initializes the
        :class:`Uncertainties.calc_uncertainties.Distribution` objects, and stores them in the list.

        :return: None
        '''
        super(UncertaintiesModel, self).__init__()
        # set up constants
        self.distributions = []
        path = os.path.dirname(os.path.realpath(__file__))
        self.my_outputs = get_outputs(self)
        self.filename = path + '\\uncertainties.csv'
        self.init_distributions(self.filename)

    # primary component method
    def execute(self):
        '''
        The primary method that OpenMDAO requires that you populate for any component with the behavior you want the
        component to have. In this case, the component is just a grouping of uncertainty variable distributions. It
        is possible to integrate this capability into the each model, but this provides a way to consolidate them
        into one location.

        On each execution, this component loops through all saved distributions, then samples them with a probability
        value (Percent Point Function) to retrieve the value that occurs at the given probability. The values are
        stored into the output attributes of the UncertaintiesModel component. See
        :class:`Uncertainties.calc_uncertainties.Distribution` for more information.

        :return: None
        '''
        # ToDo: Determine if it would be better to integrate this capability into individual model components

        # Loop through and sample all of my uncertainties
        for dist in self.distributions:
            # Get latest value from input probabilities
            probInput = getattr(self, dist.output + "_prob")
            setattr(self, dist.output, dist.sample(probInput))

    def init_distributions(self, filename):
        '''
        Inits probability and associated values from a provided CSV file. This enables you to defined the uncertain
        variables by cumulative distribution functions in two columns for each variable. One defines the variable
        probabilities and must match the Uncertainties component configured input name with an appended '_prob'.
        Second is a column with the associated values, with a column name that matches the output name configured on
        the Uncertainties component. Example table of a normal-like distribution below:

        ================== =============
        myUncertainty_prob myUncertainty
        ================== =============
        0                  10
        0.25               15
        0.5                30
        0.75               45
        1                  50
        ================== =============

        .. note:: The CSV file can include many uncertainties input as pairs of columns, and each does not need to \
        have equal rows.

        :param filename: Location of the CSV file to load
        :return: None, saves distributions into a python :class:`list`
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

if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    from test_uncertainties import test_uncertainties_component
    test_uncertainties_component()