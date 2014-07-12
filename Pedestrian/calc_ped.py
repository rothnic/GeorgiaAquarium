__author__ = 'Nick'

from Common.DecisionTreeSurrogate.DecisionTreeSurrogate import DecisionTreeSurrogate

class PedSurrogate:

    def __init__(self, trainingFile, inputCols, outputCols, netFile):
        self.surrogate = DecisionTreeSurrogate(trainingFile, inputCols, outputCols, netFile)
        self.offDays = 236
        self.onDays = 129

    def sim(self, pedsPerHourOn, pedsPerHourOff):
        avgStepsOn = self.surrogate.sim([pedsPerHourOn])
        avgStepsOff = self.surrogate.sim([pedsPerHourOff])
        yearlyStepsPerTile = (self.offDays * 7.0 * avgStepsOff) + (self.onDays * 12.0 * avgStepsOn)

        return yearlyStepsPerTile[0]


def setup_defaults():
    # set up constants
    defaults = {}
    defaults['trainingFile'] = 'pedTrainingData.csv'
    defaults['netFile'] = 'decisionTreeSurrogate.p'
    defaults['outputCols'] = ['output']
    defaults['inputCols'] = ['input']
    return defaults

# Only ran when this calc_ped is run directly
# Used for testing the functions
if __name__ == "__main__":

    # Load default values
    defaults = setup_defaults()

    # Load training data and initialize surrogate
    ps = PedSurrogate(trainingFile=defaults['trainingFile'], inputCols=defaults['inputCols'],
                       outputCols=defaults['outputCols'], netFile=defaults['netFile'])

    # Print results of input data
    print ps.sim(500, 600)