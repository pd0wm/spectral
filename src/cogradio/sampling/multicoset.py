import numpy as np
import cogradio as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self):
        print "Multicoset sampler"

    def reconstruct(self, signal):
        return [1, 2, 3]

    def generateTRx(self, M, N, L, C):
        Rc0 = np.zeros((M**2, N))
        Rc1 = np.zeros((M**2, N))

        for i in range(0, M-1):
            for j in range(0, M-1):
                sigI = C[i, :]
                sigJ = C[j, :]
