import numpy as np
import cogradio_utils as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, N):
        super(MultiCoset, self).__init__()

        sparseruler = cg.sparseruler(N)

        self.N = N
        self.M = len(sparseruler)
        self.C = cg.build_sparse_ruler_sampling_matrix(sparseruler, N)

    def sample(self, signal):
        length = int(np.floor(len(signal) / self.N))
        tmp = length * self.N
        y = np.zeros((self.M, length), dtype=np.complex64)
        for i in np.arange(0, tmp, self.N):
            y[:, i / self.N] = np.dot(np.fliplr(self.C), signal[i:(i + self.N)])
        return y
