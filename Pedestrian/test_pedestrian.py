__author__ = 'Nick'
from Pedestrian import PedestrianModel

if __name__=="__main__":
    ped = PedestrianModel()

    # Dummy sample values
    offs = range(200, 1500, 100)
    ons = range(100, 1400, 100)

    # Loop through samples and execute model
    for on, off in zip(ons, offs):
        ped.pedsPerHourOff = off
        ped.pedsPerHourOn = on
        ped.execute()
        print ped.yearlyStepsPerTile