"""
   /Energy/Sources/Solar/Solar.py
"""

import os

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float
from pyopt_driver import pyopt_driver
from openmdao.lib.casehandlers import csvcase
from pandas import read_csv
from calc_solar import calc_num_panels, calc_power, calc_cost

class SolarModel(Component):
    '''
    The SolarModel is an OpenMDAO component that wraps the actual calculations performed for the solar modeling,
    while defining the input and output attributes.
    '''
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    panelRating = Float(280.0, iotype='in', desc='panel rating')
    panelEff = Float(0.17, iotype='in', desc='panel efficiency')
    sunRadianceScalar = Float(1.0, iotype='in', desc='uncertainty around radiance')
    surfaceArea = Float(558.0, iotype='in', desc='number of panels')
    circuitLoss = Float(0.7, iotype='in', desc='circuit power loss')

    # set up outputs
    totalkWh = Float(110000.0, iotype='out', desc='yearly power output')
    solarCapitalCost = Float(150000.0, iotype='out', desc='investment cost')

    # set up constants
    panelSize = 1.42         #: Fixed value for panel size in square meters
    maxSurfaceArea = 1000.0  #: Maximum area in square meters available for installation
    sunDataTable = read_csv(path + '\\solarAtl2010.csv') #: CSV table of solar data read into Pandas object
    sunData = sunDataTable["irradiance"].values          #: Solar irradiance data read from sunDataTable

    # primary model method
    def execute(self):
        '''
        The method that OpenMDAO requires that the behavior of the model be developed in. At each model execution,
        OpenMDAO will write new values into the model's inputs, then will call this execute method. After the
        execution is complete, it will read total power and total initial capital cost information from it.

        :returns: None
        '''

        # Initial setup
        numPanels = calc_num_panels(self.surfaceArea, self.panelSize)

        # Calculate power
        self.totalkWh = calc_power(
            self.panelRating,
            self.panelEff,
            self.sunRadianceScalar,
            self.surfaceArea,
            self.circuitLoss,
            self.sunData)

        # Calculate cost
        self.solarCapitalCost = calc_cost(
            self.panelEff,
            self.surfaceArea,
            self.panelRating,
            numPanels)


class SolarOptimization(Assembly):
    '''
    Implements an assembly to contain the SolarModel component, and run optimizations on it stand-alone with the
    pyOpt plugin of optimization drivers. Implements a caserecorder so that you can investigate the results
    afterwards. This assembly will show up automatically when using openmdao gui, or can be used directly in another
    python script as you would use a regular python class.
    '''

    def configure(self):
        '''
        This method is used to implement the custom behavior of the SolarOptimization Assembly. OpenMDAO requires
        that you implement this method, and it is used to add the optimization component, the SolarModel,
        and to configure the parameters within the optimization component.

        :returns: Outputs optimization results to the console and saves all data for inputs and outputs into a CSV \
        file named 'solar_optimization.csv'.

        '''

        # Add the pyOpt driver and case recorder
        self.replace("driver", pyopt_driver.pyOptDriver())
        self.driver.recorders.append(csvcase.CSVCaseRecorder(filename='solar_optimization.csv'))

        # Add the solar model to the assembly
        self.add("sm", SolarModel())

        # Add the parameters to be used in optimization
        self.driver.add_parameter('sm.panelEff', low=.1, high=.25)
        self.driver.add_parameter('sm.panelRating', low=100, high=450)
        self.driver.add_parameter('sm.surfaceArea', low=0, high=1000)

        self.driver.add_objective('-sm.totalkWh')
        self.driver.add_constraint('sm.solarCapitalCost <= 400000.0')


if __name__ == "__main__":
    '''
    A module testing routine, executes when this python file is ran independently. For example, using Pycharm,
    right click while editing and select Run. The tests called below are alternatively ran automatically by pytest
    from test_solar if configured to do so within Pycharm.
    '''
    from test_solar import run_print_test, test_solar_non_neg, testSolarComp, testSolarClean, test_solar_optimization

    run_print_test()
    testSolarClean()
    testSolarComp()
    test_solar_non_neg()
    test_solar_optimization()

