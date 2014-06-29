__author__ = 'Nick'


def calc_power(panelRating, panelEff, sunRadianceScalar, numPanels,
               circuitLoss):
    return panelRating + panelEff + sunRadianceScalar + numPanels


def calc_cost(solarCostPerWatt, batteryCost):
    return solarCostPerWatt * 50 + batteryCost