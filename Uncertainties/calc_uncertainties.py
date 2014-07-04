__author__ = 'Nick'

import scipy.stats as st
from scipy.interpolate import interpolate
import numpy as np


def create_year():
    pass


class Distribution:
    def __init__(self, probData, valueData, output):
        self.output = output
        self.probData = probData
        self.valueData = valueData
        self.make_cdf()
        self.make_pdf()

    def sample(self, prob):
        # Sample the Percent Point Function (PPF). Given a probability it returns a value
        # expected to occur at the rate of the probability.
        return self.pdf.ppf(prob)

    def make_cdf(self):
        self.cdf = interpolate.splmake(self.valueData, self.probData, order=1)

    def make_pdf(self):
        # Divide up bins across value range to sample probability changes
        bins = np.linspace(min(self.valueData), max(self.valueData), 50)
        diff = np.zeros(len(bins))

        # Step through and calculate change in probability for values across CDF to yield PDF
        for i in range(1, len(bins) - 1):
            start = interpolate.spleval(self.cdf, bins[i])
            end = interpolate.spleval(self.cdf, bins[i + 1])
            diff[i] = end - start

        # Generate the PDF from interpolated and sampled CDF
        self.pdf = st.rv_discrete(name=self.output, values=(bins, diff))