from .source import Source
import numpy as np


class ComplexSinusoidal(Source):

    """Signal representing a couple of complex sinusoidal frequencies"""

    def __init__(self, frequencies, SNR=None):
        Source.__init__(self, frequencies, SNR)

    def generate(self, samp_freq, duration):
        signal = 0
        t = np.arange(0, np.ceil(duration * samp_freq)) / samp_freq

        for f in self.frequencies:
            signal += np.exp(2 * 1j * np.pi * f * t)

        signal = self.cmplx_white_gaussian_noise(self.SNR, signal)

        return signal
