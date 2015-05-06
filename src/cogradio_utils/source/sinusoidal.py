from .source import Source
import numpy as np
import cogradio_utils as cg


class Sinusoidal(Source):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self, frequencies, SNR=None):
        Source.__init__(self, frequencies, SNR)

    def generate(self, samp_freq, duration):
        signal = 0
        t = np.arange(0, np.ceil(duration * samp_freq)) / samp_freq
        
        for f in self.frequencies:
            signal += np.cos(2 * np.pi * f * t)

        signal = self.white_gaussian_noise(self.SNR, signal)

        return signal
