__author__ = 'Nick'

import scipy.stats as st
import numpy as np
import pandas as pd
from scipy.interpolate import interpolate

def create_year():

# Average visitors per hour input into pedestrian model per day
# SunOffExp = 5388
# MonOffExp = 3148
# TueOffExp = 1988
# WedOffExp
#
    pass


cdfInput = pd.read_csv('uncertainties.csv')
val_on = cdfInput['pedsPerHourOn']
prob_on = cdfInput['pedsPerHourOn_prob']
val_off = cdfInput['pedsPerHourOff']
prob_off = cdfInput['pedsPerHourOff_prob']
cdfInput.head()