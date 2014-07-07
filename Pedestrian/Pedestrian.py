__author__ = 'Nick'

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from calc_ped import PedSurrogate
from Common.AttributeTools.io import print_outputs
import os


class PedestrianModel(Component):
    # set up inputs
    pedsPerHourOn = Float(500.0, iotype='in', desc='panel rating')
    pedsPerHourOff = Float(800.0, iotype='in', desc='panel efficiency')

    # set up outputs
    yearlyStepsPerTile = Float(1.0, iotype='out', desc='yearly power output')

    # set up constants
    trainingFile = 'pedTrainingData.csv'
    netFile = 'trainedPedSurrogate.net'
    outputCols = 'output'
    inputCols = 'input'

    def __init__(self):
        super(PedestrianModel, self).__init__()

        # Get full paths to file co-located with this one
        path = os.path.dirname(os.path.realpath(__file__))
        trainingFile = os.path.join(path, self.trainingFile)
        netFile = os.path.join(path, self.netFile)

        # Initialize surrogate model
        self.model = PedSurrogate(trainingFile=trainingFile, inputCols=self.inputCols,
                                  outputCols=self.outputCols, netFile=netFile)

    def execute(self):
        # Initial setup
        self.yearlyStepsPerTile = self.model.sim(self.pedsPerHourOn, self.pedsPerHourOff)


def run_tests():
    comp = PedestrianModel()
    comp.execute()
    print_outputs(comp)


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    run_tests()