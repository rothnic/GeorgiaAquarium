__author__ = 'Nick'

from numba import jit
import numpy as np


@jit
def total_energy_produced(yearlyPowerProducedSolar, yearlyPowerProducedTribo, yearlyPowerProducedWind):
    return yearlyPowerProducedSolar + yearlyPowerProducedTribo + yearlyPowerProducedWind


def total_energy_consumed(baselineTotalPowerUse, totalEnergySaved, totalPowerProduced):
    return baselineTotalPowerUse - totalEnergySaved - totalPowerProduced


def total_energy_cost(elecUtilityRate, totalPowerConsumed):
    return elecUtilityRate * totalPowerConsumed


def original_energy_cost(elecUtilityRate, baselineTotalPowerUse):
    return elecUtilityRate * baselineTotalPowerUse


def total_energy_saved(hydraulicPowerUse, baselineOceanVoyPowerUse):
    return baselineOceanVoyPowerUse - hydraulicPowerUse


@jit
def calc_roi(totalInitialInvestment, totalEnergyCost, originalEnergyCost):
    # 1 year, 5 year, 10 year, 15 year, 20 year, 25 year
    # Expected break even point
    years = np.array(range(0, 100, 1))
    costs = years * originalEnergyCost
    actualCost = years * totalEnergyCost
    costDiff = costs - actualCost

    return costDiff - totalInitialInvestment


@jit
def get_break_even(totalInitialInvestment, totalEnergyCost, originalEnergyCost):
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


@jit
def total_capital_cost(solarCapitalCost, triboCapitalCost, windCapitalCost, hydraulicCapitalCost):
    return solarCapitalCost + triboCapitalCost + windCapitalCost + hydraulicCapitalCost


@jit
def total_utility(futureRoi, expectedReturn, investmentYears, totalInitialInvestment):
    # take into account near term versus long term returns

    baselineProfit = totalInitialInvestment * (1 + expectedReturn * investmentYears)
    # totalUtility = futureRoi / (1 + expectedReturn) ** investmentYears

    # return a ratio of how the future ROI compares to simply investing the money in the market
    return futureRoi / (baselineProfit - totalInitialInvestment)
