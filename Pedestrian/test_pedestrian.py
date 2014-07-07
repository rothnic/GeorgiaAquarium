__author__ = 'Nick'
from Pedestrian import PedestrianModel
import pytest

def test_samples():
    ped = PedestrianModel()

    # Dummy sample values
    offs = range(200, 1500, 100)
    ons = range(100, 1400, 100)
    yearlyStepsOut = []
    # Loop through samples and execute model
    for on, off in zip(ons, offs):
        ped.pedsPerHourOff = off
        ped.pedsPerHourOn = on
        ped.execute()
        yearlyStepsOut.append(ped.yearlyStepsPerTile)

    assert min(yearlyStepsOut) > 0