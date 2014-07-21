__author__ = 'Nick'


import pandas as pd
import numpy as np

class Lights():
    def __init__(self, numBulbs, scaleRatio, bulbWatts, bulbCost, bulbLife, hoursOnPerDay, current):
        '''
        Lights is a reuseable and general class for describing the lights configuration for any Georgia Aquarium
        exhibit. The class can be used as part of the higher level exhibit class to come up with a total power use
        and total investment and recurring costs for the exhibit.

        :param numBulbs: Number of light bulbs/fixtures for this configuration
        :param scaleRatio: The number of new bulbs needed to replace one old one
        :param bulbWatts: The rating of the bulbs for this configuration
        :param bulbCost: The cost in dollars of a single bulb
        :param bulbLife: The lifespan in hours for the configured bulb
        :param hoursOnPerDay:
        :param current:
        :return:
        '''
        self.numBulbs = numBulbs
        self.bulbWatts = bulbWatts
        self.bulbCost = bulbCost
        self.bulbLife = bulbLife
        self.hoursOnPerDay = hoursOnPerDay
        self.current = current
        self.scaleRatio = scaleRatio
        self.table = pd.DataFrame(data={'numBulbs':self.numBulbs,
                                        'scaleRatio':self.scaleRatio,
                                        'bulbWatts':self.bulbWatts,
                                        'bulbCost':self.bulbCost,
                                        'bulbLife':self.bulbLife,
                                        'hoursOnPerDay': self.hoursOnPerDay,
                                        'current': self.current})
    @property
    def initial_cost(self):
        '''
        Calculates the first year cost of the lighting configuration. This takes into account if the lighting
        configuration is the nominal one, and returns a cost of zero, making the assumption that we already have
        lights at the current moment in time and do not need to immediately replace them.

        :return: The cost for the current configuration for the initial year of analysis.
        '''
        cur = self.table['current'].values
        out = np.zeros(len(cur),)
        curIdx = cur == True
        if len(out[cur == True]) > 0:
            out[cur == True] = 0.0
        if len(out[cur != True]) > 0:
            out[cur != True] = self.recurring_cost
        return out

    @property
    def recurring_cost(self):
        '''
        Calculates the cost required at the recurrance_period.

        .. note:: Assumes all lights go out at once.

        :return: :class:`pandas.Series` of length equal to the number of configurations defined, where each value \
        is the cost in dollars each time you have to replace the lights.
        '''
        return self.table['numBulbs'] * self.table['bulbCost'] * self.table['scaleRatio']

    @property
    def recurrance_period(self):
        '''
        Calculates the number of years required before replacing a bulb

        :return: :class:`pandas.Series` of length equal to the number of configurations defined, where each value \
        represents the length in years until the associated lights will need to be replaced
        '''
        return (self.table['bulbLife'] / self.table['hoursOnPerDay']) / 365


    def yearly_cost(self, maxYears):
        '''
        Yearly cost of the lighting configuration over the length of maxYears.

        :param maxYears: The number of years out to calculate the recurring cost
        :return: :class:`numpy.ndarray` with length of maxYears
        '''

        periods = self.recurrance_period
        cost = self.recurring_cost
        init_cost = self.initial_cost

        yearArray = np.array(range(1, maxYears+1))

        costs = np.zeros((len(periods), len(yearArray)))


        for i,years in enumerate(periods):
            costs[i, yearArray % years < 1] = cost[i]
            costs[i,0] += init_cost[i]

        return costs


    @property
    def power_per_year(self):
        '''
        Calculates the total amount of power in kWh for the current lighting configuration

        :return: Total amount of power in kWh used by the lights
        '''
        return (self.table['bulbWatts']/1000) * self.table['hoursOnPerDay'] * 365

    def print_config(self):
        '''
        Prints the configuration to console.

        :return: None
        '''
        print self.table


if __name__=='__main__':
    lc = Lights([25],[2], [25],[25],[25],[25],[True])
    #lc = LightConfig([25], [25], [25], [25], [25,25])
    lc = Lights([25,5], [2,1.5], [25,5], [25,5], [10000,5], [12,5], [True, True])
    lc.print_config()
    print 'recurrence period: ' + str(lc.recurrance_period)
    print 'initial_cost: ' + str(lc.initial_cost)
    print 'power used per year: ' + str(lc.power_per_year)
    print 'yearly costs'
    print lc.yearly_cost(10)