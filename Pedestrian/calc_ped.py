__author__ = 'Nick'

from Common.DecisionTreeSurrogate.DecisionTreeSurrogate import DecisionTreeSurrogate

class PedSurrogate:

    def __init__(self, offDays, onDays, trainingFile, inputCols, outputCols, regressorFile):
        '''
        Initializer for the Pedestrian surrogate model. This model reads in data from an agent-based pedestrian model
        for the Georgia Aquarium built in AnyLogic. The AnyLogic model is limited from integrating with this one due
        to university version restrictions, and takes much too long to run. It is beneficial to run the AnyLogic
        model over the design space ahead of time, then generate a surrogate model from the parametric output data.
        The surrogate model currently uses a random forest tree surrogate that has been pre-trained on the parametric
        data. When the PedSurrogate class is provided the netFile, which is a trained model saved to disk,
        it initializes the surrogate and it is then ready for execution. This particular surrogate model wraps the
        decision tree surrogate because we need two samples from it for every execution. One sample is for the on
        season pedestrian rates, and one is for the off season pedestrian rates.

        :param trainingFile: The original input data. This is used even in post training for initializing the surrogate
        :param inputCols: A list of string values representing the input columns in the trainingFile
        :param outputCols: A list of string values representing the output columns in the trainingFile
        :param netFile: A trained model that has been saved to disk via pickling
        :return: The initialized PedSurrogate object
        '''
        self.surrogate = DecisionTreeSurrogate(trainingFile, inputCols, outputCols, regressorFile)
        self.offDays = offDays
        self.onDays = onDays

    def sim(self, pedsPerHourOn, pedsPerHourOff):
        '''
        The only method of the PedSurrogate class. It has two parameters it takes, which are the uncertainty values
        representing the pedestrians per hour in the on season, and the pedestrians per hour in the off season. These
        are used to calculate the average steps we could expect on a triboelectric tile in a given year.

        .. Note: Assumes 7 hours per day for off season, and 12 hours per day for on season

        :param pedsPerHourOn: Average pedestrians per hour in the on season
        :param pedsPerHourOff: Average pedestrians per hour in the off season
        :return: Number of steps we would expect per triboelectric tile on average for a given year
        '''
        # ToDo: Ideally, the steps per tile would vary based on the tile position. Would require changes in anylogic

        avgStepsOn = self.surrogate.sim([pedsPerHourOn])
        avgStepsOff = self.surrogate.sim([pedsPerHourOff])
        yearlyStepsPerTile = (self.offDays * 7.0 * avgStepsOff) + (self.onDays * 12.0 * avgStepsOn)

        return yearlyStepsPerTile[0]


def setup_defaults():
    '''
    Setup method called that is used to create a python dict of default values for initializing the surrogate model

    :return: Python dict with keys of 'trainingFile', 'netFile', 'outputCols', and 'inputCols'
    '''
    import os
    path = os.path.dirname(os.path.realpath(__file__))

    # set up constants
    defaults = {}
    defaults['trainingFile'] = os.path.join(path, 'pedTrainingData.csv')
    defaults['netFile'] = os.path.join(path, 'decisionTreeSurrogate.p')
    defaults['outputCols'] = ['output']
    defaults['inputCols'] = ['input']
    return defaults

# Only ran when this calc_ped is run directly
# Used for testing the functions
if __name__ == "__main__":

    # Load default values
    defaults = setup_defaults()

    # Load training data and initialize surrogate
    ps = PedSurrogate(236, 139, trainingFile=defaults['trainingFile'], inputCols=defaults['inputCols'],
                       outputCols=defaults['outputCols'], regressorFile=defaults['netFile'])

    # Print results of input data
    print ps.sim(500, 600)