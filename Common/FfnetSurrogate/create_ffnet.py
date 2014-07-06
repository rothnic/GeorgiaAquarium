__author__ = 'Nick'

from FfnetSurrogate import FfnetSurrogate

# Load csv
# specify inputs
# specify outputs
#



def neural_from_csv(trainFile, inputCols, outputCols):
    surr = FfnetSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train([len(inputCols), 20, len(outputCols)])
    surr.test()
    return surr


def create_surrogate():

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

    return neural_from_csv(trainFile, inputCols, outputCols)

def test_surrogate(surrogate):
    surrogate.sim([800,20,0.6,20,1300,0.1,1600])

if __name__=="__main__":
    surr = create_surrogate()
    test_surrogate(surr)