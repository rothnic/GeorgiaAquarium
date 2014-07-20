__author__ = 'Nick'

import os

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float
import pandas as pd


from Common.AttributeTools.io import print_outputs
from calc_cost import *

class CostModel(Component):
    '''
    The CostModel exists as an integrating component between the various possible improvements and the aquarium
    and exhibits. This architecture allows for each improvement and exhibit to implement a very straightforward
    interface of producing power measures and capital investment costs for the given design configuration. The
    CostModel aggregates all of these values up and provides the overall comparison metrics of the entire design.
    '''

    # get our current directory
    path = os.path.dirname(os.path.realpath(__file__))

    # set up inputs
    hydraulicCapitalCost = Float(100000.0, iotype='in', desc='cost of making change to hydraulics')
    windCapitalCost = Float(100000.0, iotype='in', desc='cost of implementing wind energy')
    solarCapitalCost = Float(100000.0, iotype='in', desc='cost of implementing solar energy')
    triboCapitalCost = Float(100000.0, iotype='in', desc='cost of implementing tribo energy')
    elecUtilityRate = Float(0.1, iotype='in', desc='cost of electricity')
    baselineTotalPowerUse = Float(27765028.90, iotype='in', desc='total GA power use')
    baselineOceanVoyPowerUse = Float(19948604.08, iotype='in', desc='total ocean voyager power use')
    hydraulicPowerUse = Float(19648604.08, iotype='in', desc='total ocean voyager power use')
    yearlyPowerProducedSolar = Float(100.0, iotype='in', desc='solar power produced for given investment')
    yearlyPowerProducedWind = Float(100.0, iotype='in', desc='wind power produced for given investment')
    yearlyPowerProducedTribo = Float(100.0, iotype='in', desc='tribo power produced for given investment')

    # set up outputs
    totalPowerProduced = Float(1.0, iotype='out', desc='yearly power output for GA')
    totalPowerConsumed = Float(1.0, iotype='out', desc='yearly power output for GA')
    totalInitialInvestment = Float(1.0, iotype='out', desc='investment cost')
    totalEnergyCost = Float(1.0, iotype='out', desc='what is paid for energy to a utility company')
    totalEnergySaved = Float(1.0, iotype='out', desc='how much energy we saved with modifications, excluding produced')
    originalEnergyCost = Float(1.0, iotype='out', desc='what we would have paid for energy to a utility company')
    breakEvenYear = Float(1.0, iotype='out', desc='year at which we break even for investment')
    year1Roi = Float(1.0, iotype='out', desc='how much we make for the investment in year 1')
    year5Roi = Float(1.0, iotype='out', desc='how much we make for the investment in year 5')
    year10Roi = Float(1.0, iotype='out', desc='how much we make for the investment in year 10')
    year20Roi = Float(1.0, iotype='out', desc='how much we make for the investment in year 20')
    year30Roi = Float(1.0, iotype='out', desc='how much we make for the investment in year 30')
    totalUtility = Float(1.0, iotype='out', desc='overall, how good is the solution?')

    # set up constants
    expectedReturn = 0.1 # S&P 500 average return
    investmentYears = 10 # Number of years to wait before comparing which decision to make

    # primary model method
    def execute(self):
        '''
        Implements the behavior portion of the OpenMDAO component. Each time all of the models are executed with this
        method, all of the energy consumed, produced, and the capital invested is used to compare against the current
        operations of the Georgia Aquarium. With these values, the cost model provides how much was saved,
        the break even year, the return on investment over many years, and the total utility of the design.

        :return: None
        '''

        # Calculate total power produced
        self.totalPowerProduced = total_energy_produced(self.yearlyPowerProducedSolar,
                                                        self.yearlyPowerProducedTribo,
                                                        self.yearlyPowerProducedWind)

        # Calculate how much we power usage we saved due to modifications, excluding power production
        self.totalEnergySaved = total_energy_saved(self.hydraulicPowerUse, self.baselineOceanVoyPowerUse)

        # Calculate total power consumed
        self.totalPowerConsumed = total_energy_consumed(self.baselineTotalPowerUse, self.totalEnergySaved,
                                                        self.totalPowerProduced)

        # Calculate the total paid out in energy costs, excluding renewable investment costs
        self.totalEnergyCost = total_energy_cost(self.elecUtilityRate, self.totalPowerConsumed)

        # Calculate how much we would have paid for energy
        self.originalEnergyCost = original_energy_cost(self.elecUtilityRate, self.baselineTotalPowerUse)

        # Calculate how much we paid to decrease energy usage
        self.totalInitialInvestment = total_capital_cost(self.solarCapitalCost, self.triboCapitalCost,
                                                         self.windCapitalCost, self.hydraulicCapitalCost)

        # Get the year where we break even for this solution
        self.breakEvenYear = get_break_even(self.totalInitialInvestment, self.totalEnergyCost, self.originalEnergyCost)

        # Get return on investment after x number of years
        roi = calc_roi(self.totalInitialInvestment, self.totalEnergyCost, self.originalEnergyCost)
        self.year1Roi = roi[1]
        self.year3Roi = roi[3]
        self.year5Roi = roi[5]
        self.year10Roi = roi[10]
        self.year20Roi = roi[20]
        self.year30Roi = roi[30]

        # Calculate the quality of this solution
        self.totalUtility = total_utility(self.year10Roi, self.expectedReturn, self.investmentYears,
                                          self.totalInitialInvestment)


if __name__ == "__main__":
    # Module test routine, executes when this python file is ran independently
    # For example, using Pycharm, right click while editing and select Run
    from test_cost import *
    test_break_even()
    test_cost_component()
    test_model_with_print()
    test_roi()