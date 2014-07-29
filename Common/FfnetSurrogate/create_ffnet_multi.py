__author__ = 'Nick'

from FfnetSurrogate import FfnetSurrogate


def neural_from_csv(trainFile, inputCols, outputCols):
    surr = FfnetSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train(num_neurons=30)
    surr.test()
    return surr


def create_surrogate():

    inputCols = [
        'pumpFlow',
        'pumpRatedHead',
        'pumpRatedRpm',
        'pumpRunRpm',
        'pumpEff',
        'flowLossCoeff',
        'heatExchFlowLossCoef',
        'heatExchValveOpen',
        'denitFlowLossCoef',
        'ozoneFlowLossCoef',
        'ozoneValveOpen',
        'denitValveOpen',
        'deaerationFlowLossCoef'
    ]

    outputCols = [
        'pumpEffOut',
        'pumpPower',
        'pumpFlow',
        'headExchFlow',
        'heatExch2Flow',
        'sandPowerIn',
        'sandFlow',
        'heatExchPowerIn',
        'juncPowerIn',
        'ozone1_6Flow',
        'ozone1_6PowerIn',
        'denitrifictionPowerIn',
        'denitrificationFlow',
        'denitificationPowerOut',
        'ozone7_12Flow',
        'deareationPowerIn',
        'deareationFlow',
        'powerIn',
        'bypassFlow',
        'deareationPowerOut',
        'sandPowerOut',
        'heatExchPowerOut'
    ]

    trainFile = 'hydroSandTraining.csv'

    return neural_from_csv(trainFile, inputCols, outputCols)


if __name__=="__main__":
    surr = create_surrogate()
