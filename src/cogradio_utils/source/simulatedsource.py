from .source import Source
import numpy as np
import cogradio_utils as cg


class SimulatedSource(Source):

    """Source parent for simulating sources"""

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(SimulatedSource, self).__init__(samp_freq)
        self.frequencies = frequencies
        self.SNR = SNR

    def white_gaussian_noise(self, SNR, signal):
        if not SNR:
            return signal

        if type(signal[0]) is np.complex64:
            return self.cmplx_white_gaussian_noise(SNR, signal)
        else:
            return self.real_white_gaussian_noise(SNR, signal)

    def real_white_gaussian_noise(self, SNR, signal):
        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = signal / np.std(signal) * np.sqrt(cg.invert_db(SNR))
        return scaled_signal + noise

    def cmplx_white_gaussian_noise(self, SNR, signal):
        noise_r = np.random.normal(0, 0.5, len(signal))
        noise_i = 1j * np.random.normal(0, 0.5, len(signal))

        noise = np.random.rayleigh(size=(len(signal), 1))
        scaled_signal = signal * np.std(np.abs(noise)) / np.std(signal) * np.sqrt(cg.invert_db(SNR))
        return scaled_signal + noise_r + noise_i
