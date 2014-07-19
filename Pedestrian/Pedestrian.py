__author__ = 'Nick'

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from calc_ped import PedSurrogate, setup_defaults
from Common.AttributeTools.io import print_outputs


class PedestrianModel(Component):
    """
    The PedestrianModel class represents the Pedestrian flow through the Georgia Aquarium. The model was originally
    developed using AnyLogic, which includes powerfully pedestrian simulation capabilities. This OpenMDAO component
    implements a surrogate of the original Anylogic model. It extends the OpenMDAO Component.
    """

    # set up inputs
    pedsPerHourOn = Float(600.0, iotype='in', desc='panel rating')
    pedsPerHourOff = Float(500.0, iotype='in', desc='panel efficiency')

    # set up outputs
    yearlyStepsPerTile = Float(47180.0, iotype='out', desc='yearly power output')

    # set up constants
    offDays = 236      #: number of off season days in one year
    onDays = 139       #: number of on season days in one year

    # primary model method
    def __init__(self):
        '''
        Extend the OpenMDAO component init method only so that we don't have to reload the model file each time it is
        executed. This might be considered bad practice, but is necessary to reduce run time. There could be a better
        way to avoid this problem.

        :return: Initialized OpenMDAO SurrogateModel component object
        '''
        # ToDo: See if there is a better way to initialize the surrogate without having to extend the constructor

        super(PedestrianModel, self).__init__() #: Execute the parent OpenMDAO Component method, then do our own

        # Get full paths to file co-located with this one
        defaults = setup_defaults()
        path = os.path.dirname(os.path.realpath(__file__))
        trainingFile = os.path.join(path, defaults['trainingFile'])
        netFile = os.path.join(path, defaults['netFile'])

        # Initialize surrogate model
        self.model = PedSurrogate(offDays=self.offDays, onDays=self.onDays,
                                  trainingFile=trainingFile, inputCols=defaults['inputCols'],
                                  outputCols=defaults['outputCols'], netFile=netFile)

    # primary model method
    def execute(self):
        """
        Execute is the primary method that every openMDAO component must implement. Each time the model is ran by
        openMDAO, the execute method is called. In this case, the Pedestrian model reads the openMDAO input
        attributes, then executes the surrogate model with these values. The surrogate model is trained within the
        __init__ method, so the trained model is executed quickly. The inputs are both the on season and off season
        values for how many expected visitors are expected on average in an hour. These values were derived from data
        provided by Georgia Aquarium. These values are used to come up with an aggregate number of steps per tile
        we'd expected over a years time.

        :return: yearly steps per single triboelectric tile
        """
        self.yearlyStepsPerTile = self.model.sim(self.pedsPerHourOn, self.pedsPerHourOff)

if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    from test_pedestrian import test_samples, run_tests_with_print
    run_tests_with_print()
    test_samples()