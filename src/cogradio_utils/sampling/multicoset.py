import numpy as np
import cogradio_utils as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, N, mode="msr"):
        Sampler.__init__(self)
        self.N = N
        self.mode = mode
        sparseruler = cg.sparseruler(N)
        self.C = cg.build_C(sparseruler, N)
        self.M = len(sparseruler)

    def generateC(self):
        return self.C

    def sample(self, signal):
        if self.mode == "msr":
            return self.__msr_sample(signal)
        else:
            raise NotImplementedError("Unsupported mode: " + self.mode)

    def __msr_sample(self, signal):
        length = int(np.floor(len(signal) / self.N))
        tmp = length * self.N
        y = np.zeros((self.M, length), dtype=np.complex64)
        for i in np.arange(0, tmp, self.N):
            y[:, i / self.N] = np.dot(np.fliplr(self.C), signal[i:(i + self.N)])
        return y
