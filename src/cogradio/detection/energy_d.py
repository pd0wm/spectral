from .detector import Detector
import numpy as np
import cogradio as cg

class energy_d(Detector):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self, Threshold):
        self.Threshold = Threshold

    def detect(self, rx):
        # Rx is symmetric, create the Covariance Matrix
        # assuming that E[x] = 0
        print("Energy_Detection Threshold: " + str(self.Threshold))

        ys = cg.fft(rx)
        primary = np.zeros(len(ys))
        print(max(ys))
        for i in range(len(ys)):
            if ys[i] > self.Threshold:
                primary[i] = 1

        return primary
















