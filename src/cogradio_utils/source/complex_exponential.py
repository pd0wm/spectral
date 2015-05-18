from .simulatedsource import SimulatedSource
import numpy as np


class ComplexExponential(SimulatedSource):

    """Signal representing a couple of complex exponential frequencies"""

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(ComplexExponential, self).__init__(frequencies, samp_freq, SNR=SNR)

    def generate(self, no_samples):
        signal = np.zeros(no_samples)
        t = np.arange(0, no_samples) / float(self.samp_freq)

        for f in self.frequencies:
            signal += np.exp(2 * 1j * np.pi * f * t)

        signal = self.cmplx_white_gaussian_noise(self.SNR, signal)

        return signal
