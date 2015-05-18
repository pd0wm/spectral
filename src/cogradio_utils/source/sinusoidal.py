from .simulatedsource import SimulatedSource
import numpy as np


class Sinusoidal(SimulatedSource):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(Sinusoidal, self).__init__(frequencies, samp_freq, SNR=SNR)

    def generate(self, no_samples):
        signal = 0
        t = np.arange(0, no_samples) / float(self.samp_freq)

        for f in self.frequencies:
            signal += np.cos(2 * np.pi * f * t)

        signal = self.white_gaussian_noise(self.SNR, signal)

        return signal
