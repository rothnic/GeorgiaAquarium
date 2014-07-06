__author__ = 'Nick'

from Common.DecisionTreeSurrogate.DecisionTreeSurrogate import DecisionTreeSurrogate

# Load csv
# specify inputs
# specify outputs
#



def decision_tree_from_csv(trainFile, inputCols, outputCols):
    surr = DecisionTreeSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train(300)
    return surr


def init_surrogate():

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

    surr = decision_tree_from_csv(trainFile, inputCols, outputCols)
    surr.test()
    return surr

def test_surrogate(surr):
    surr.predict([800, 20, 0.6, 20, 1300, 0.1, 1600])