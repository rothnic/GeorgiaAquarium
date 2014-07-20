__author__ = 'Nick'

import scipy.stats as st
from scipy.interpolate import interpolate
import numpy as np

class Distribution:
    '''
    The Distribution class sets up a construct for loading uncertainty data that was generated as user input to
    define the probability distribution, interpolating between the given points to create the CDF, then sampling
    across the CDF to generate the PDF. The PDF is then used to generate a scipy :class:`~scipy.stats.rv_discrete`
    distribution object. The scipy distribution can then be later used for sampling the distribution.
    '''
    def __init__(self, probData, valueData, output):
        '''
        Initializes the Distribution object with the user created probability data and the name of the uncertainty
        variable that the distribution represents.

        :param probData: A :class:`numpy.ndarray` of probabilities for the uncertainty
        :param valueData: A :class:`numpy.ndarray` of values associated with the probabilities for the uncertainty
        :param output: The name of the uncertainty as a string
        :return: initialized Distribution object
        '''
        self.output = output
        self.probData = probData
        self.valueData = valueData
        self.make_cdf()
        self.make_pdf()

    def sample(self, prob):
        '''
        Samples the initialized distribution to retrieve the value with an occurrence of the provided probability.
        This is referred to as the Percent Point Function. See :meth:`scipy.stats.rv_discrete.ppf` for more
        information.

        :param prob: Value between 0 and 1, representing the probability of occurrence of the returned value
        :return: The value associated with the provided probability
        '''

        # Sample the Percent Point Function (PPF). Given a probability it returns a value
        # expected to occur at the rate of the probability.
        return self.pdf.ppf(prob)

    def make_cdf(self):
        '''
        Generates a CDF from user provided data by using the :func:`scipy.interpolate.splmake` function

        :return: representation of the spline interpolated CDF that was initialized into the Distribution object
        '''
        self.cdf = interpolate.splmake(self.valueData, self.probData, order=1)

    def make_pdf(self):
        '''
        Generates a PDF from the spline-interpolated CDF. This method crudely calculates the derivative of the CDF by
        calculating the change in likelihood across the distribution. Next, it provides the bins used for sampling
        the CDF, along with the the difference in probability between the bins to :class:`~scipy.stats.rv_discrete`,
        and in return receives the :class:`~scipy.stats.rv_discrete` object, then saves it into the
        :class:`~Uncertainties.calc_uncertainties.Distribution` object for later sampling using the
        :py:meth:`~Uncertainties.calc_uncertainties.Distribution.sample` method.

        :return: None
        '''

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