from .reconstructor import Reconstructor
import cogradio_utils as cg
import numpy as np
import scipy.linalg
import scipy.sparse
import scipy as sp

class Wessel(Reconstructor):

    """Implementation of Wessel's adaption of the ariananda algorithm"""
    def __init__(self, N, L, C=None):
        Reconstructor.__init__(self)
        self.N = N
        self.L = L
        sparseruler = cg.sparseruler(N)
        if C is None:
            self.C = cg.build_C(sparseruler, N)
        self.M = self.C.shape[0]
        self.R = self.constructR()
        self.Rinv = sp.linalg.pinv(self.R)

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        Ry = self.cross_correlation_signals(signal)
        rx = self.Rinv.dot(Ry)
        return rx

    def cross_correlation_signals(self, signal):
        Ry = np.zeros((self.M ** 2 * (2 * self.L - 1)), dtype=np.complex64)
        for i in range(self.M):
            for j in range(self.M):
                Ry[(i * self.M + j)*(2 * self.L - 1):(i * self.M + j + 1)*(2 * self.L - 1)] = self.N*np.correlate(signal[i, :],
                                                  signal[j, :],
                                                  mode='full')
        return Ry

    def constructR(self):
        # Construct "Decimation" matrix
        D = np.zeros((2*self.L-1, 2*self.N*self.L-1),dtype=np.complex64)
        for i in range(0, 2*self.L-1):
            D[i, i*self.N] = 1       

        # Calculate filter cross correlations
        rcc = np.zeros((self.M**2, 2*self.N-1), dtype=np.complex64)
        for i in range(0, self.M):
            for j in range(0, self.M):
                rcc[i*self.M+j] = np.correlate(self.C[i,:], self.C[j,:], mode='full')        
        # Build Rcc toeplitz jetschers
        Rcc = np.zeros((self.N*self.L*2-1, self.N*self.L*2-1), dtype=np.complex64)
        R = np.zeros((self.M**2*(2*self.L-1), 2*self.N*self.L-1), dtype=np.complex64)

        for i in range(0, self.M**2):
            column = np.concatenate((rcc[i,:], np.zeros(2*self.N*self.L - 2*self.N, dtype=np.complex64)))
            row = np.insert(np.zeros(self.N*self.L*2-2, dtype=np.complex64), 0, rcc[i,0])

            Rcc = sp.linalg.toeplitz(column, row)
            R[i*(2*self.L-1):((i+1)*(2*self.L-1)), :] = np.dot(D,Rcc)                    
        return R
