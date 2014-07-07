__author__ = 'Nick'

from FfnetSurrogate import FfnetSurrogate


def neural_from_csv(trainFile, inputCols, outputCols):
    surr = FfnetSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    print len(inputCols)
    print len(outputCols)
    surr.train([len(inputCols), 10, len(outputCols)])
    surr.test()
    return surr


def create_surrogate():

    inputCols = [
        "input"
    ]

    outputCols = [
        "output"
    ]

    trainFile = 'pedTrainingData.csv'

    return neural_from_csv(trainFile, inputCols, outputCols)


if __name__=="__main__":
    surr = create_surrogate()
    surr.sim([500])
    surr.save('trainedPedSurrogate.net')
