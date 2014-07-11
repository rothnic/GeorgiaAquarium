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
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    panelRating = Float(280.0, iotype='in', desc='panel rating')
    panelEff = Float(0.17, iotype='in', desc='panel efficiency')
    sunRadianceScalar = Float(1.0, iotype='in', desc='uncertainty around radiance')
    surfaceArea = Float(558.0, iotype='in', desc='number of panels')
    solarCostPerWatt = Float(1.50, iotype='in', desc='solar cost')
    batteryCost = Float(0.0, iotype='in', desc='cost of batteries')
    circuitLoss = Float(0.7, iotype='in', desc='circuit power loss')

    # set up outputs
    totalkWh = Float(110000.0, iotype='out', desc='yearly power output')
    solarCapitalCost = Float(150000.0, iotype='out', desc='investment cost')

    # set up constants
    panelSize = 1.42
    maxSurfaceArea = 1000.0  # Square meters
    sunDataTable = read_csv(path + '\\solarAtl2010.csv')
    sunData = sunDataTable["irradiance"].values

    def execute(self):
        # Initial setup
        numPanels = calc_num_panels(self.surfaceArea, self.panelSize)
        self.solarCostPerWatt = (-68.33333 + 7.5 * self.panelEff) * self.surfaceArea * 0.027945

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
            self.solarCostPerWatt,
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
        # Add the pyOpt driver and case recorder
        self.replace("driver", pyopt_driver.pyOptDriver())
        self.driver.recorders.append(csvcase.CSVCaseRecorder())

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
    from test_solar import run_print_test, test_solar_non_neg, testSolarComp, testSolarClean

    run_print_test()
    testSolarClean()
    testSolarComp()
    test_solar_non_neg()

