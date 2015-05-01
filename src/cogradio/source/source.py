import numpy as np


class Source(object):

    """Source parent object for spectrum sensing"""

    def __init__(self, frequencies, SNR):
        self.frequencies = frequencies
        self.SNR = SNR

    def generate(self, samp_freq, duration):
        raise NotImplementedError("Implement this method.")

    def white_gaussian_noise(self, SNR, signal):
        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = np.std(
            noise) / np.std(signal) * (np.sqrt(10 ** (SNR / 10.0))) * signal
        return scaled_signal + noise
