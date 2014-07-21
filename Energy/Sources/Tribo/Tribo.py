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
    '''
    The TriboModel is a wrapper for a power and cost calculation in regard to implementing a tile-based triboelectric
    system. The PaveGen solution was the primary intended use, although there is very little available information
    for it. There are some articles, such as _this: http://www.theguardian.com/sustainable-business/power-generating-tiles-renewable-energy
    one that seems to cause confusion on how to calculate the power generation. The approach taken is to create a
    detailed simulation of the pedestrian movement through the aquarium to estimate the number of steps we would see
    on a given tile, then use that information in the calculation of power generation.

    The current assumption for power calculation is that the quoted 7 watts per step is only over a short period of
    time, like 1 second. You can use this to calculate what that is in kWh. This can be used with the yearly steps
    per tile to provide some performance output for a design decision on the number of tiles, along with the cost
    impact of that decision.

    Relies on input values from the :class:`~Pedestrian.Pedestrian.PedestrianModel` for use in calculating the power
    generation.
    '''

    # set up inputs
    tileCount = Float(20.0, iotype='in', desc='number of tiles')
    pedStepsPerTile = Float(260000.0, iotype='in', desc='expected steps per tile')
    tileEff = Float(0.9, iotype='in', desc='tribo efficiency (percent)')
    tileUnitCost = Float(800.0, iotype='in', desc='unit cost of a single tile')
    mgtTileUnitCost = Float(3000.0, iotype='in', desc='unit cost of a management tile')
    tilePower = Float(0.007, iotype='in', desc='wattage produced per step (kWh)')

    # set up outputs
    totalkWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    triboCapitalCost = Float(40000.0, iotype='out', desc='investment cost ($)')

    # set up constants
    # timePerStep and wattsPerStep were used to calculate the expected value
    timePerStep = 1.0  #: The duration of power generation for one step

    # primary model method
    def execute(self):
        '''
        The method for an OpenMDAO component that is required to be filled out with the internal behavior,
        and is called each time OpenMDAO has changed the input values. After execution, the new output values are
        then read from the component. This component executes to functions; one to calculate power, and one to
        calculate the initial capital cost associated with the configuration of the input values.

        :return: None
        '''

        # Calculate power
        self.totalkWh = calc_power(
            self.tileCount,
            self.pedStepsPerTile,
            self.tileEff,
            self.tilePower,
            self.timePerStep)

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
        '''
        This method must be filled in with the desired configuration for any custom OpenMDAO Assembly. This Assembly
        is used to load the :class:`~Energy.Sources.Tribo.Tribo.TriboModel` for execution, sets up a :mod:`pyOpt`
        optimizer, configures a CSV recorder to record inputs and outputs to tribo_optimization.csv, then configures
        parameters, an objective, and a constraint. This isolated optimization can be used to ensure the model is
        working correctly before integrating it into a larger model.
        '''

        # Add the pyOpt driver and case recorder
        self.replace("driver", pyopt_driver.pyOptDriver())
        self.driver.recorders.append(csvcase.CSVCaseRecorder(filename='tribo_optimization.csv'))

        # Add the solar model to the assembly
        self.add("tm", TriboModel())

        # Add the parameters to be used in optimization
        self.driver.add_parameter('tm.tileCount', low=1, high=1000)
        self.driver.add_parameter('tm.tileEff', low=.7, high=.98)
        self.driver.add_parameter('tm.tilePower', low=.0001, high=.01)

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