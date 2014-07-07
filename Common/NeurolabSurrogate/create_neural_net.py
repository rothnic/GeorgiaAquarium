__author__ = 'Nick'

from NeurolabSurrogate import NeurolabSurrogate

# Load csv
# specify inputs
# specify outputs
#



def neural_from_csv(trainFile, inputCols, outputCols):
    surr = NeurolabSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train([10,len(outputCols)])
    #print surr.sim([800,20,0.6,20,1300,0.1,1600])
    surr.test()


if __name__=="__main__":

    inputCols = [
        "ratedSpeed",
        "flc",
        "ratedEff",
        "ratedHead",
        "ratedFlow",
        "csa",
        "runSpeed"
    ]

    outputCols = [
        "pumpHp",
        "totalFlowOut",
        "pskFlow2",
        "pskFlow1",
        "pIn",
        "pOut1"
    ]

    trainFile = 'hydroTraining.csv'

    neural_from_csv(trainFile, inputCols, outputCols)