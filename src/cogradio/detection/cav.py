from .detector import Detector
import numpy as np
import cogradio as cg
from scipy.linalg import toeplitz
from scipy import stats

class CAV(Detector):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self):
        Detector.__init__(self)

    def detect(self, rx):
        # Rx is symmetric, create the Covariance Matrix
        # assuming that E[x] = 0
        li = (np.ceil(rx.size/2))-1
        ui = rx.size-1

        Cx = toeplitz(rx[li:ui],None)

        T1 = np.sum(np.absolute(Cx))
        T2 = np.matrix.trace(np.absolute(Cx));

        # calculate treshold
        L = (rx.size+1)/2
        # Number of samples we used to estimate rx
        Ns = L
        Pfa = 0.05
        gamma = (1+(L-1)*np.sqrt(2/(Ns*np.pi)))/(1-stats.norm.sf(Pfa)*np.sqrt(2/Ns))
        if(gamma < (T1/T2)):
            return True
        else:
            return False
