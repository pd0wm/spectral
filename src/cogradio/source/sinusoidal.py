from .source import Source
import numpy as np
import cogradio

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
            signal = self.white_gaussian_noise(self.SNR, signal)

        return signal

    def white_gaussian_noise(self, SNR, signal):
        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = np.std(noise)/np.std(signal)*(np.sqrt(10**(SNR/10.0))) * signal
        return scaled_signal + noise
