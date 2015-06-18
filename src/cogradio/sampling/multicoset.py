import numpy as np
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, S, N, M):
        super(MultiCoset, self).__init__()
        self.C = self.build_sampling_matrix(S, N, M)
        self.N = self.C.shape[1]
        self.M = self.C.shape[0]

    def sample(self, x):
        length = x.shape[0]
        offset = length % self.N
        if offset != 0:
            x = x[:-offset]
        x = np.reshape(x.T, (self.N, -1), order='F')
        y = np.dot(self.C, x)
        return y

    def build_sampling_matrix(self, intervals, N, M):
        C = np.zeros((M, N), np.complex128)
        for i, j in enumerate(intervals):
            C[i, j] = 1
        return C
