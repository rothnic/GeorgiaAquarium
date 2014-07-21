__author__ = 'Nick'

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, Array
import numpy as np
from numpy import float as numpy_float


class LightingModel(Component):
    '''
    The LightingModel is a wrapper for a power and cost calculation in regard to replacing current lighting fixtures
    with more energy
    '''

    # set up inputs
    numBulbs = Float(1.0, iotype='in', desc='number of bulbs to replace')

    # set up outputs
    yearlykWhNominal = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    recurringCostsNominal = Array(np.array([[0.0,0.0,6000,0.0,0.0,6000,0.0,0.0,6000,0.0]]), dtype=numpy_float,
                                  shape=(1,10), iotype='out')

    yearlykWh = Float(1.0, iotype='out', desc='yearly power output (kWh)')
    recurringCosts = Array(np.array([[0.0,0.0,6000,0.0,0.0,6000,0.0,0.0,6000,0.0]]), dtype=numpy_float,
                           shape=(1,10), iotype='out')

    # set up constants
    years = 10   #: Years to project out recurring costs

    # initialization
    def __init__(self, lightObjNew, lightObjOld):
        '''
        Overrides the initialization of the OpenMDAO Component class. The purpose is to provide a way to customize
        and reuse this class for many different exhibits.

        :param lightObjNew: Configured :class:`~Common.Lighting.calc_lighting.Lights` class for new bulbs
        :param lightObjOld: Configured :class:`~Common.Lighting.calc_lighting.Lights` class for old bulbs
        :return: Initialized :class:`~Common.Lighting.Lighting.LightingModel` object
        '''
        super(LightingModel, self).__init__()
        self.lightObjNew = lightObjNew
        self.lightObjOld = lightObjOld
        self.nominalkWh = self.lightObjOld.power_per_year[0]
        self.nominalRecurring = self.lightObjOld.yearly_cost(self.years)
        self.maxBulbs = self.lightObjOld.numBulbs

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
        # Reset values for nominal case, which is always the same
        self.yearlykWhNominal = self.nominalkWh

        # Apply penalty if optimizer chooses too many bulbs

        # Reconfigure new lighting config with more or less bulbs
        self.lightObjNew.numBulbs = self.numBulbs
        self.yearlykWh = self.lightObjNew.power_per_year[0]


        # Calculate cost
        self.recurringCostsNominal = self.nominalRecurring
        self.recurringCosts = self.lightObjNew.yearly_cost(self.years)


if __name__=='__main__':
    from test_lighting import *
    test_lighting_model()
    test_lights_cost()
    test_lights_initial()
    test_lights_power_year()
    test_lights_recurrance()

