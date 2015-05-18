from .simulatedsource import SimulatedSource
import numpy as np
import scipy.signal as sp


class Rect(SimulatedSource):

    """Signal representing a rectangle in the spectrum"""

    def __init__(self, frequencies, widths, samp_freq, SNR=None):
        super(Rect, self).__init__(frequencies, samp_freq, SNR=SNR)
        self.widths = widths

    def generate(self, no_samples):
        signal = 0
        t = np.arange(0, no_samples) / float(self.samp_freq)
        duration = t[-1]
        for f, width in zip(self.frequencies, self.widths):
            component = 2 * width * np.sinc(2 * width * (t - duration / 2))
            carrier = np.sin(2 * np.pi * f * t)

            component *= carrier
            signal += component

        window = sp.hamming(no_samples)
        signal *= window

        signal = self.white_gaussian_noise(self.SNR, signal)

        return signal
