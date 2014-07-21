__author__ = 'Nick'

from Common.Lighting.Lighting import LightingModel
from Common.Lighting.calc_lighting import Lights
from Common.AttributeTools.io import print_outputs


def init_ocean_voyager_lighting(numLightsNominal):
    pass



if __name__=='__main__':

    lsOld = Lights([40], [1], [1000], [180], [10000], [12], [True])
    lsNew = Lights([30], [1.5], [120], [712], [50000], [12], [False])
    lm = LightingModel(lsNew, lsOld)
    lm.execute()
    print_outputs(lm)