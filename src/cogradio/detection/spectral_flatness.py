from .detector import Detector
import numpy as np


class SPFL(Detector):

    """Detection using spectrall flatness Method"""

    def __init__(self):
        Detector.__init__(self)

    def detect(self, rx, binwidth, treshold):
        normalized_rx = rx/rx.size
        normalized_spectrum = np.abs(np.fft.fftshift(np.fft.fft(normalized_rx))) / rx.size
        standard_deviation = np.zeros((normalized_spectrum.size))

        for i in range(normalized_spectrum.size):
            begin = max(0, int(i-binwidth/2))
            end = min(normalized_spectrum.size, i+binwidth/2-1)
            standard_deviation[i] = np.std(normalized_spectrum[begin:end])

        return standard_deviation > treshold
