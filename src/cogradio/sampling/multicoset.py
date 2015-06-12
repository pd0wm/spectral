import numpy as np
import cogradio as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, N, C=None):
        super(MultiCoset, self).__init__()
        if C is not None:
            self.C = C
        else:
            sparseruler = cg.sparseruler(N)
            self.C = cg.build_sparse_ruler_sampling_matrix(sparseruler, N)

        self.N = self.C.shape[1]

    def sample(self, x):
        length = x.shape[0]
        offset = length % self.N
        if offset != 0:
            x = x[:-offset]
        x = np.reshape(x.T, (self.N, -1), order='F')
        y = np.dot(self.C, x)
        return y
