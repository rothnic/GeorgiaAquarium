__author__ = 'Nick'

from numba import jit
import numpy as np


#@jit
def total_energy_produced(yearlyPowerProducedSolar, yearlyPowerProducedTribo, yearlyPowerProducedWind):
    '''
    Sums up the energy produced from all components with this design configuration.

    :param yearlyPowerProducedSolar: Solar power production in kWh
    :param yearlyPowerProducedTribo: Tribo power production in kWh
    :param yearlyPowerProducedWind: Wind power production in kWh
    :return: Total power production in kWh
    '''
    return yearlyPowerProducedSolar + yearlyPowerProducedTribo + yearlyPowerProducedWind


def total_energy_consumed(baselineTotalPowerUse, totalEnergySaved, totalPowerProduced):
    '''
    Total energy consumed by all of the power consuming components for this design configuration.

    :param baselineTotalPowerUse: Power use of aquarium in the nominal configuration, no changes
    :param totalEnergySaved: Total energy that was saved, when compared to nominal case
    :param totalPowerProduced: Total energy consumed in kWh for one year with this design configuration
    :return:
    '''
    return baselineTotalPowerUse - totalEnergySaved - totalPowerProduced


def total_energy_cost(elecUtilityRate, totalPowerConsumed):
    '''
    Calculates the energy cost for this design configuration considering the power usage and savings.

    :param elecUtilityRate: Cost per kWh in dollars
    :param totalPowerConsumed: Total power consumed over the entire year for this design configuration
    :return: Total cost in dollars for energy for the entire year
    '''
    return elecUtilityRate * totalPowerConsumed


def original_energy_cost(elecUtilityRate, baselineTotalPowerUse):
    '''
    Calculates the energy cost for the nominal cost without modifications to anything, for comparison to the current
    design.

    :param elecUtilityRate: Cost per kWh in dollars
    :param baselineTotalPowerUse: The total power use for one year in the nominal configuration
    :return: The total power cost for in one year for the nominal configuration
    '''
    return elecUtilityRate * baselineTotalPowerUse


def total_energy_saved(hydraulicPowerUse, baselineOceanVoyPowerUse):
    '''
    Total energy saved in comparison between the baseline case and the current configuration of the design.

    :param hydraulicPowerUse: The power use in kWh for this design for an entire year
    :param baselineOceanVoyPowerUse: The power use in kWh for an entire year for the nominal configuration
    :return: Total energy saved for this configuration over the nominal case in one year in kWh
    '''
    return baselineOceanVoyPowerUse - hydraulicPowerUse


#@jit
def calc_roi(totalInitialInvestment, totalEnergyCost, originalEnergyCost):
    '''
    Calculates the return on investment for each year, for 100 years. This can be used to sample the return on
    investment at any desired year.

    :param totalInitialInvestment: Total cost of the changes that have been made for the initial year in dollars
    :param totalEnergyCost: Total cost of the energy for this configuration for one year in dollars
    :param originalEnergyCost: The energy cost for one year in dollars for the nominal case
    :return: A :class:`numpy.ndarray` of 100 return on investment values in dollars, associated with each year
    '''

    # 1 year, 5 year, 10 year, 15 year, 20 year, 25 year
    # Expected break even point
    years = np.array(range(0, 100, 1))
    costs = years * originalEnergyCost
    actualCost = years * totalEnergyCost
    costDiff = costs - actualCost

    return costDiff - totalInitialInvestment


#@jit
def get_break_even(totalInitialInvestment, totalEnergyCost, originalEnergyCost):
    '''
    Calculates the point at which we break even for the initial investment.

    :param totalInitialInvestment: Total cost in dollars for this design configuration.
    :param totalEnergyCost: Total energy cost in dollars for the year in dollars
    :param originalEnergyCost: Cost of energy for one year in dollars for the nominal configuration
    :return: The year where we break even for the investment based on the savings
    '''
    # How much we save each month because of investment
    monthlySavings = (originalEnergyCost - totalEnergyCost) / 12

    # Initialize variables for finding when we break even
    totalSavings = 0 - totalInitialInvestment
    months = 0.0

    if monthlySavings > 0:
        while totalSavings < 0:
            totalSavings += monthlySavings
            months += 1
    else:
        months = -1
    # return decimal years
    return months / 12.0


#@jit
def total_capital_cost(solarCapitalCost, triboCapitalCost, windCapitalCost, hydraulicCapitalCost):
    '''
    Calculates the total cost of this design configuration investment based on all changes that were made.

    :param solarCapitalCost: Total investment cost for solar in dollars
    :param triboCapitalCost: Total investment cost for tribo in dollars
    :param windCapitalCost: Total investment cost for wind in dollars
    :param hydraulicCapitalCost: Total investment cost for hydraulics in dollars
    :return: The total investment cost for this design configuration in dollars
    '''
    return solarCapitalCost + triboCapitalCost + windCapitalCost + hydraulicCapitalCost


#@jit
def total_utility(futureRoi, expectedReturn, investmentYears, totalInitialInvestment):
    '''
    Calculates the total utility of this configuration based on current and future returns. This should provide a way
    to compare solutions together that might provide very little initial turns, but really good future returns,
    and vice-versa.

    :param futureRoi: The return on investment for the year that we are interested in
    :param expectedReturn: The return percentage if we were to just invest the money instead
    :param investmentYears: The number of years to look into the future for the investment returns
    :param totalInitialInvestment: The total investment required for this current design configuration
    :return: The total utility of this design (no units)
    '''

    # take into account near term versus long term returns
    baselineProfit = totalInitialInvestment * (1 + expectedReturn * investmentYears)
    # totalUtility = futureRoi / (1 + expectedReturn) ** investmentYears

    # return a ratio of how the future ROI compares to simply investing the money in the market
    return futureRoi / (baselineProfit - totalInitialInvestment)
