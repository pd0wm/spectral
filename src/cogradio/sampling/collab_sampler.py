import numpy as np
import cogradio as cg
from .sampling import Sampler


class CollabSampler(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, S, N):
        super(CollabSampler, self).__init__()

        self.S = S
        self.N = N
        self.M = len(S)
        self.C = cg.build_sparse_ruler_sampling_matrix(S, N)

    def sample(self, signal):
        length = int(np.floor(len(signal) / self.N))
        tmp = length * self.N
        y = np.zeros((self.M, length), dtype=np.complex64)
        for i in np.arange(0, tmp, self.N):
            y[:, i / self.N] = np.dot(np.fliplr(self.C), signal[i:(i + self.N)])
        return y
