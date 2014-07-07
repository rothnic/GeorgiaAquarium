__author__ = 'Nick'

from Common.FfnetSurrogate.FfnetSurrogate import FfnetSurrogate

class PedSurrogate:
    def __init__(self, trainingFile, inputCols, outputCols, netFile):
        self.surrogate = FfnetSurrogate(trainingFile, inputCols, outputCols, netFile)
        self.offDays = 236
        self.onDays = 129

    def sim(self, pedsPerHourOn, pedsPerHourOff):
        avgStepsOn = self.surrogate.sim([pedsPerHourOn])
        avgStepsOff = self.surrogate.sim([pedsPerHourOff])

        yearlyStepsPerTile = self.offDays * avgStepsOff + self.onDays * avgStepsOn

        return yearlyStepsPerTile[0]


# Only ran when this calc_ped is run directly
# Used for testing the functions
if __name__ == "__main__":
    from Common.NeurolabSurrogate.NeurolabSurrogate import NeurolabSurrogate

    # Location of training and surrogate files
    trainFile = 'pedTrainingData.csv'
    netFile = 'pedSurrogate.net'

    # Load training data and initialize surrogate
    sur = NeurolabSurrogate(trainingFile=trainFile, inputCols='', outputCols='output', netFile=netFile)

    # Print results of input data
    print "Surrogate Testing Results"
    sur.print_sim(xrange(50, 1500, 100))