"""
   /Energy/Sources/Wind/Wind.py
"""

import os

import pandas as pd
from openmdao.main.api import Component, Assembly
from pyopt_driver import pyopt_driver
from openmdao.lib.casehandlers import csvcase
from openmdao.lib.datatypes.api import Float

from calc_wind import calc_cost, calc_power
from Common.AttributeTools.io import print_outputs


class WindModel(Component):
    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    turbineCount = Float(3.0, iotype='in', desc='turbine count')
    turbineRating = Float(3000.0, iotype='in', desc='turbine power rating (kW)')
    turbineEff = Float(0.4, iotype='in', desc='turbine efficiency (percent)')
    windSpeedScalar = Float(1.0, iotype='in', desc='uncertainty around wind speed (scalar)')
    windCostPerWatt = Float(1.5, iotype='in', desc='wind cost per capacity ($/watt)')
    circuitLoss = Float(0.75, iotype='in', desc='circuit power loss (percent)')
    airDensity = Float(1.23, iotype='in', desc='air density (kg/m^3)')
    bladeLength = Float(1.524, iotype='in', desc='turbine blade length (m)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    windCapitalCost = Float(1.0, iotype='out', desc='investment cost ($)')

    # set up constants
    windDataTable = pd.read_csv(path + '\\windAtl.csv')
    windData = windDataTable["windSpeed"].values

    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.bladeLength,
            self.turbineEff,
            self.airDensity,
            self.turbineCount,
            self.circuitLoss,
            self.windData)

        # Calculate cost
        self.windCapitalCost = calc_cost(
            self.windCostPerWatt,
            self.turbineRating,
            self.turbineCount)


class WindOptimization(Assembly):
    '''
    Implements an assembly to contain the WindModel component, and run optimizations on it stand-alone with the
    pyOpt plugin of optimization drivers. Implements a caserecorder so that you can investigate the results
    afterwards. This assembly will show up automatically when using openmdao gui, or can be used directly in another
    python script as you would use a regular python class.
    '''

    def configure(self):
        # Add the pyOpt driver and case recorder
        self.replace("driver", pyopt_driver.pyOptDriver())
        self.driver.recorders.append(csvcase.CSVCaseRecorder(filename='wind_optimization.csv'))

        # Add the solar model to the assembly
        self.add("wm", WindModel())

        # Add the parameters to be used in optimization
        self.driver.add_parameter('wm.bladeLength', low=.1, high=3.5)
        self.driver.add_parameter('wm.turbineRating', low=100, high=5000)
        self.driver.add_parameter('wm.turbineCount', low=0, high=12)

        self.driver.add_objective('-wm.totalkWh')
        self.driver.add_constraint('wm.windCapitalCost <= 400000.0')


if __name__ == "__main__":
    '''
    A module testing routine, executes when this python file is ran independently. For example, using Pycharm,
    right click while editing and select Run. The tests called below are alternatively ran automatically by pytest
    from test_wind if configured to do so within Pycharm.
    '''
    from test_wind import run_print_test, test_wind_component, test_wind_power_calc, test_wind_optimization
    run_print_test()
    test_wind_component()
    test_wind_power_calc()
    test_wind_optimization()