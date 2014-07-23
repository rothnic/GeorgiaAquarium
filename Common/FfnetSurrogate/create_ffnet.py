__author__ = 'Nick'

from FfnetSurrogate import FfnetSurrogate


def neural_from_csv(trainFile, inputCols, outputCols):
    surr = FfnetSurrogate(trainingFile=trainFile, inputCols=inputCols, outputCols=outputCols)
    surr.train(25)
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
        'sandPowerOut',
        'sandPowerIn',
        'sandFlow',
        'heatExchPowerIn',
        'heatExchPowerOut',
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
        'deareationPowerOut'
    ]

    trainFile = 'hydroSandTraining.csv'

    return neural_from_csv(trainFile, inputCols, outputCols)


if __name__=="__main__":
    surr = create_surrogate()
    #surr.sim([500])
    surr.save('trainedHydroSurrogate.net')
