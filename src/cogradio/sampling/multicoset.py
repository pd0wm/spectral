import numpy as np
import cogradio as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, N):
        super(MultiCoset, self).__init__()
        self.C = self.generate_C(N)
        self.N = self.C.shape[1]

    def generate_C(self, N):
        sparseruler = cg.sparseruler(N)
        return cg.build_sparse_ruler_sampling_matrix(sparseruler, N)

    def sample(self, x):
        length = x.shape[0]
        offset = length % self.N
        if offset != 0:
            x = x[:-offset]
        x = np.reshape(x.T, (self.N, -1), order='F')
        y = np.dot(self.C, x)
        return y
