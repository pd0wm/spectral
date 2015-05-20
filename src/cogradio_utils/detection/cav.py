from .detector import Detector
import numpy as np
import cogradio_utils as cg
from scipy.linalg import toeplitz
from scipy import stats

class CAV(Detector):

    """Signal representing a couple of sinusoidal frequencies"""

    def __init__(self):
        Detector.__init__(self)

    def detect(self, rx):
        return None
