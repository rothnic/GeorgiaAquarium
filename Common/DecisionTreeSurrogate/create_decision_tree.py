__author__ = 'Nick'

from Common.DecisionTreeSurrogate.DecisionTreeSurrogate import DecisionTreeSurrogate
import os

def decision_tree_from_csv(trainFile, inputCols, outputCols):
    surr = DecisionTreeSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train(300)
    return surr


def init_surrogate():

    inputCols = [
        "input"
    ]

    outputCols = [
        "output"
    ]

    trainFile = 'pedTrainingData.csv'

    path = os.path.dirname(os.path.realpath(__file__))
    trainPath = os.path.join(path, trainFile)
    surr = decision_tree_from_csv(trainPath, inputCols, outputCols)
    surr.test()
    return surr

if __name__=="__main__":
    from test_decisiontree_surrogate import test_decision_tree
    test_decision_tree()