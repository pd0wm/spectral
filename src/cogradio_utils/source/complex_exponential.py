from .simulatedsource import SimulatedSource
import numpy as np


class ComplexExponential(SimulatedSource):

    """Signal representing a couple of complex exponential frequencies"""

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(ComplexExponential, self).__init__(frequencies, samp_freq, SNR=SNR)

    def generate(self, no_samples):
        t = np.arange(0, no_samples) / self.samp_freq
        signals = [np.exp(2j * np.pi * f * t) for f in self.frequencies]
        signal = reduce(np.add, signals)

        return self.white_gaussian_noise(self.SNR, signal)
