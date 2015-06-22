from .simulatedsource import SimulatedSource
import numpy as np
import scipy as sp


class Rect(SimulatedSource):

    """
    Signal representing a number of rectangles in the frequency domain.

    Args:
        frequencies: A list of center frequencies of the blocks.
        widths: A list of widths of the rectangles
        samp_freq: Sample frequency
        SNR: Signal to Noise ratio of the output signal
    """

    def __init__(self, frequencies, widths, samp_freq, SNR=None):
        super(Rect, self).__init__(frequencies, samp_freq, SNR=SNR)
        self.widths = widths

    def generate(self, no_samples):
        """
        Generator function that generates a signal with rectangular
        frequency components specified on object creation.

        Args:
            no_sampls: Number of samples to generate

        Returns:
            Generated samples with a Signal to Noise ratio as specified on
            object creation.
        """
        t = np.arange(0, no_samples) / self.samp_freq
        duration = t[-1]

        signals = []
        for f, width in zip(self.frequencies, self.widths):
            component = 2 * width * np.sinc(2 * width * (t - duration / 2))
            carrier = np.sin(2 * np.pi * f * t)
            signals.append(component * carrier)

        signal = reduce(np.add, signals)
        signal *= sp.signal.hamming(len(signal))
        return self.white_gaussian_noise(self.SNR, signal)
