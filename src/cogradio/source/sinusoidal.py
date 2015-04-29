from .source import Source
import numpy as np


class Sinusoidal(Source):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self, frequencies, SNR=0):
        Source.__init__(self, frequencies, SNR)

    def generate(self, samp_freq, duration):
        signal = 0
        t = np.arange(0, np.ceil(duration*samp_freq)) / samp_freq
        for f in self.frequencies:
            signal += np.sin(2 * np.pi * f * t)

        if self.SNR != 0:
            pass

        return signal
