__author__ = 'Nick'

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float

from calc_ped import Surrogate, PedSurrogate


class PedestrianModel(Component):
    # set up inputs
    pedsPerHourOn = Float(500.0, iotype='in', desc='panel rating')
    pedsPerHourOff = Float(800.0, iotype='in', desc='panel efficiency')

    # set up outputs
    yearlyStepsPerTile = Float(1.0, iotype='out', desc='yearly power output')

    # set up constants
    trainingFile = '\\pedTrainingData.csv'
    netFile = '\\pedSurrogate.net'
    outputCols = 'output'

    def __init__(self):
        super(PedestrianModel, self).__init__()

        surrogate = Surrogate(trainingFile=self.trainingFile, inputCols='',
                              outputCols=self.outputCols, netFile=self.netFile)
        self.model = PedSurrogate(surrogate)

    def execute(self):
        # Initial setup
        self.yearlyStepsPerTile = self.model.sim(self.pedsPerHourOn, self.pedsPerHourOff)