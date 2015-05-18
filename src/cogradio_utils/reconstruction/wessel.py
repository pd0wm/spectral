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
        # get height of C
        self.M = self.C.shape[0] 
        self.R = self.constructR()
        self.Rinv = sp.linalg.pinv(self.R)

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        ry = self.cross_correlation_signals(signal)
        rx = self.Rinv.dot(ry)
        return rx

    def cross_correlation_signals(self, signal):
        ry = np.zeros((self.M ** 2 * (2 * self.L - 1)), dtype=np.complex64)
        for i in range(self.M):
            for j in range(self.M):
                begin = (i * self.M + j)*(2 * self.L - 1)
                end = begin + 2*self.L-1
                ry[begin:end] = self.N*np.correlate(signal[i, :],  signal[j, :], mode='full')
        return ry

    def constructR(self):
        # Construct "decimation" matrix
        D = np.zeros((2*self.L-1, 2*self.N*self.L-1), dtype=np.complex64)
        for i in range(0, 2*self.L-1):
            D[i, i*self.N] = 1

        # Calculate M^2 filter cross correlations
        cross_correlations = np.zeros((self.M**2, 2*self.N-1), dtype=np.complex64)
        for i in range(0, self.M):
            for j in range(0, self.M):
                cross_correlations[i*self.M +
                    j] = np.correlate(self.C[i, :], self.C[j, :], mode='full')
        # Build Rcc toeplitz jetschers, M^2 times
        # containing "toeplitz" filter cross correlation 
        Rcc = np.zeros(
            (self.N*self.L*2-1, self.N*self.L*2-1), dtype=np.complex64)

        # Stack all M^2 Rcc matrices
        R = np.zeros(
            (self.M**2*(2*self.L-1), 2*self.N*self.L-1), dtype=np.complex64)

        # zero pad cross correlation to create a 2NL-1x2NL-1 matrix  
        column_padding = np.zeros(2*self.N*self.L - 2*self.N, dtype=np.complex64)
        row_padding = np.zeros(self.N*self.L*2-2, dtype=np.complex64)
        for i in range(0, self.M**2):            
            column = np.concatenate((cross_correlations[i, :], column_padding))
            row = np.insert(row_padding, 0, cross_correlations[i, 0])
            Rcc = sp.linalg.toeplitz(column, row)
            R[i*(2*self.L-1):((i+1)*(2*self.L-1)), :] = np.dot(D, Rcc)
        return R
