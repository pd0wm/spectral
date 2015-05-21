from .simulatedsource import SimulatedSource
import numpy as np


class Sinusoidal(SimulatedSource):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(Sinusoidal, self).__init__(frequencies, samp_freq, SNR=SNR)

    def generate(self, no_samples):
        t = np.arange(0, no_samples) / float(self.samp_freq)
        signals = [np.cos(2 * np.pi * f * t) for f in self.frequencies]
        signal = reduce(np.add, signals)

        return self.white_gaussian_noise(self.SNR, signal)
