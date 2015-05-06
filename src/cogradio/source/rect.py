from .source import Source
import numpy as np
import scipy.signal as sp
import cogradio


class Rect(Source):

    """Signal representing a rectangle in the spectrum"""

    def __init__(self, frequencies, widths, SNR=None):
        Source.__init__(self, frequencies, SNR)
        self.widths = widths

    def generate(self, samp_freq, duration):
        signal = 0
        t = np.arange(0, np.ceil(duration * samp_freq)) / samp_freq
        
        for f, width in zip(self.frequencies, self.widths):
            component = 2 * width * np.sinc(2 * width * (t - duration / 2))
            carrier = np.sin(2 * np.pi * f * t)
            
            component *= carrier
            signal += component

        window = sp.hamming(duration * samp_freq)
        signal *= window

        signal = self.white_gaussian_noise(self.SNR, signal)

        return signal
