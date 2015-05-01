from .reconstructor import Reconstructor
import numpy as np


class CrossCorrelation(Reconstructor):

    """Implementation of ariananda2012 algorithm"""

    def __init__(self, N, M, C, F_s, chunk_size):
        Reconstructor.__init__(self)
        self.N = N
        self.M = M
        self.C = C
        self.chunk_size = chunk_size

    def reconstruct(self, signal):
        pass

    def cross_correlation_signals(self, signal):
        R = np.zeros((self.M**2, 2*self.chunk_size-1))
        for i in range(self.M):
            for j in range(self.M):
                R[i * self.M + j] = np.correlate(signal[i, :],
                                                 signal[j, :],
                                                 mode='full')
        return R

    def cross_correlation_filters(self):
        R = np.zeros((self.M**2, self.N, 2))
        
        return R
