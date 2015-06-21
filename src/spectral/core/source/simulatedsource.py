from .source import Source
import numpy as np
import spectral as spec


class SimulatedSource(Source):

    """
    Base class for all simulated sources. Provides helper functions
    for adding noise to the signal.

    Args:
        frequencies: List of frequnecies that will be generated
        samp_freq: Sample Frequency
        SNR: Signal to Noise ratio of the output signal
    """

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(SimulatedSource, self).__init__(samp_freq)
        self.frequencies = frequencies
        self.SNR = SNR

    def white_gaussian_noise(self, SNR, signal):
        """
        Function to add noise to a signal. Checks if the input signal
        is complex or real valued and calls the right helper function.

        Args:
            SNR: Signal to noise ratio of the desired output signal
            signal: Input signal

        Returns:
            Output signal with the desired Signal to noise Ratio.
        """

        if not SNR:
            return signal

        if np.iscomplex(signal).any():
            return self.cmplx_white_gaussian_noise(SNR, signal)
        else:
            return self.real_white_gaussian_noise(SNR, signal)

    def real_white_gaussian_noise(self, SNR, signal):
        """
        Function to add noise to a real valued signal. It generates
        a constant amount of noise and scales the input signal to
        achieve the desired Sinal to Noise ratio.

        Args:
            SNR: Signal to noise ratio of the desired output signal
            signal: Real valued input signal

        Returns:
            Output signal with the desired Signal to Noise ratio
        """

        noise = np.random.normal(0, 1, len(signal))
        scaled_signal = signal / np.std(signal) * np.sqrt(spec.core.invert_db(SNR))
        return scaled_signal + noise

    def cmplx_white_gaussian_noise(self, SNR, signal):
        """
        Function to add noise to a complex valued signal. It generates
        a constant amount of noise for the complex and the real part
        and scales the input signal to achieve the desired Sinal to Noise ratio.

        Args:
            SNR: Signal to noise ratio of the desired output signal
            signal: Complex valued input signal

        Returns:
            Output signal with the desired Signal to Noise ratio
        """

        noise_r = np.random.normal(0, 0.5, len(signal))
        noise_i = 1j * np.random.normal(0, 0.5, len(signal))

        noise = np.random.rayleigh(size=(len(signal), 1))
        scaled_signal = signal * np.std(np.abs(noise)) / np.std(signal) * np.sqrt(spec.core.invert_db(SNR))
        return scaled_signal + noise_r + noise_i
