from .source import Source
import numpy as np
import scipy as sp
import cogradio


class Rect(Source):

    """Signal representing a rectangle in the spectrum"""

    def __init__(self, frequencies, widths, SNR=0):
        Source.__init__(self, frequencies, SNR)
        self.widths = widths

    def generate(self, samp_freq, duration):
        signal = 0
        t = np.arange(0, np.ceil(duration * samp_freq)) / samp_freq
        for f, width in zip(self.frequencies, self.widths):
            signal += 2 * width * np.sinc(2 * width * (t - duration/2))

        window = sp.signal.hamming(duration * samp_freq)
        signal *= window

        if self.SNR != 0:
            signal = self.white_gaussian_noise(self.SNR, signal)

        return signal

    def white_gaussian_noise(self, SNR, signal):
        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = np.std(
            noise) / np.std(signal) * (np.sqrt(10 ** (SNR / 10.0))) * signal
        return scaled_signal + noise
