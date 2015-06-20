from .simulatedsource import SimulatedSource
import numpy as np


class Sinusoidal(SimulatedSource):

    """
    Signal representing a number of sinusoidal frequencies

    Args:
        frequencies: A list of frequencies that will be present in the output signal
        samp_freq: Sample frequency
        SNR: Signal to Noise ratio of the output signal
    """

    def __init__(self, frequencies, samp_freq, SNR=None):
        super(Sinusoidal, self).__init__(frequencies, samp_freq, SNR=SNR)

    def generate(self, no_samples):
        """
        Generator function that generates a signal with the frequency
        components specified on object creation.

        Agrs:
            no_samples: Number of samples to generate

        Returns:
            Generated samples with a Signal to Noise ratio as specified on
            object creation.
        """
        t = np.arange(0, no_samples) / self.samp_freq
        signals = [np.cos(2 * np.pi * f * t) for f in self.frequencies]
        signal = reduce(np.add, signals)

        return self.white_gaussian_noise(self.SNR, signal)
