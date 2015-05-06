from .detector import Detector
import numpy as np
import cogradio as cg

class CAV(Detector):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self):
        Detector.__init__(self, frequencies, SNR)

    def detect(self, rx):
        # Rx is symmetric, create the Covariance Matrix
        # assuming that E[x] = 0
        li = (np.ceil(rx.size/2))-1
        ui = rx.size-1

        
        Cx = np.toeplitz
        print("Detect: CAV")

