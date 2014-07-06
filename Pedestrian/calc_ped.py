__author__ = 'Nick'

from Common.NeurolabSurrogate.NeurolabSurrogate import Surrogate


class PedSurrogate:
    def __init__(self, surrogate):
        self.surrogate = surrogate
        self.offDays = 236
        self.onDays = 129

    def sim(self, pedsPerHourOn, pedsPerHourOff):
        avgStepsOn = self.surrogate.sim(pedsPerHourOn)
        avgStepsOff = self.surrogate.sim(pedsPerHourOff)

        yearlyStepsPerTile = self.offDays * avgStepsOff + self.onDays * avgStepsOn

        return yearlyStepsPerTile

# Only ran when this calc_ped is run directly
# Used for testing the functions
if __name__ == "__main__":
    # Location of training and surrogate files
    trainFile = 'pedTrainingData.csv'
    netFile = 'pedSurrogate.net'

    # Load training data and initialize surrogate
    sur = Surrogate(trainingFile=trainFile, inputCols='', outputCols='output', netFile=netFile)

    # Print results of input data
    print "Surrogate Testing Results"
    sur.print_sim(xrange(50, 1500, 100))