"""
   /Energy/Sources/Tribo/Tribo.py
"""

from openmdao.main.api import Component, Assembly
from openmdao.lib.datatypes.api import Float
from pyopt_driver import pyopt_driver
from openmdao.lib.casehandlers import csvcase

from Common.AttributeTools.io import print_outputs
from calc_tribo import calc_cost, calc_power


class TriboModel(Component):
    # set up inputs
    tileCount = Float(20.0, iotype='in', desc='number of tiles')
    pedStepsPerTile = Float(50.0, iotype='in', desc='expected steps per tile')
    tileEff = Float(0.9, iotype='in', desc='tribo efficiency (percent)')
    tileUnitCost = Float(800.0, iotype='in', desc='unit cost of a single tile')
    mgtTileUnitCost = Float(800.0, iotype='in', desc='unit cost of a management tile')
    tilekWh = Float(0.002, iotype='in', desc='power produced per step (kWh)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    triboCapitalCost = Float(40000.0, iotype='out', desc='investment cost ($)')


    def execute(self):
        # Calculate power
        self.totalkWh = calc_power(
            self.tileCount,
            self.pedStepsPerTile,
            self.tileEff,
            self.tilekWh)

        # Calculate cost
        self.triboCapitalCost = calc_cost(
            self.tileUnitCost,
            self.tileCount,
            self.mgtTileUnitCost)


class TriboOptimization(Assembly):
    '''
    Implements an assembly to contain the TriboModel component, and run optimizations on it stand-alone with the
    pyOpt plugin of optimization drivers. Implements a caserecorder so that you can investigate the results
    afterwards. This assembly will show up automatically when using openmdao gui, or can be used directly in another
    python script as you would use a regular python class.
    '''

    def configure(self):
        # Add the pyOpt driver and case recorder
        self.replace("driver", pyopt_driver.pyOptDriver())
        self.driver.recorders.append(csvcase.CSVCaseRecorder(filename='tribo_optimization.csv'))

        # Add the solar model to the assembly
        self.add("tm", TriboModel())

        # Add the parameters to be used in optimization
        self.driver.add_parameter('tm.tileCount', low=1, high=1000)
        self.driver.add_parameter('tm.tileEff', low=.7, high=.98)
        self.driver.add_parameter('tm.tilekWh', low=.0001, high=.01)

        self.driver.add_objective('-tm.totalkWh')
        self.driver.add_constraint('tm.triboCapitalCost <= 400000.0')



if __name__ == "__main__":
    '''
    A module testing routine, executes when this python file is ran independently. For example, using Pycharm,
    right click while editing and select Run. The tests called below are alternatively ran automatically by pytest
    from test_tribo if configured to do so within Pycharm.
    '''
    from test_tribo import test_tribo_openmdao_model, test_tribo_optimization

    test_tribo_openmdao_model()
    test_tribo_optimization()