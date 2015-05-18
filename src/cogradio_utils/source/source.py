import numpy as np
import cogradio_utils as cg


class Source(object):

    """Source parent object for spectrum sensing"""

    def __init__(self, frequencies, SNR):
        self.frequencies = frequencies
        self.SNR = SNR

    def generate(self, samp_freq, duration):
        raise NotImplementedError("Implement this method.")

    def white_gaussian_noise(self, SNR, signal):
        if not SNR:
            return signal

        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = signal / np.std(signal) * np.sqrt(cg.invert_db(SNR))
        return scaled_signal + noise

    def cmplx_white_gaussian_noise(self, SNR, signal):
        if not SNR:
            return signal

        noise_r = np.random.normal(0, 0.5, len(signal))
        noise_i = 1j * np.random.normal(0, 0.5, len(signal))

        noise = np.random.rayleigh(size=(len(signal), 1))
        scaled_signal = signal * np.std(np.abs(noise)) / np.std(signal) * np.sqrt(cg.invert_db(SNR))
        return scaled_signal + noise_r + noise_i
