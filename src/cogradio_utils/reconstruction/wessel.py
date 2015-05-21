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

        # Use caching if available
        self.R = self.constructR()
        print "Rank R", np.linalg.matrix_rank(self.R)
        print "Full?", self.R.shape
        self.R_pinv = self.calc_pseudoinverse(self.R)

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        ry = self.N * self.cross_correlation_signals(signal)
        ry_stacked = ry.ravel()
        rx = self.R_pinv.dot(ry_stacked)
        return rx

    def constructR(self):
        # Construct "decimation" matrix
        D = np.zeros((2*self.L-1, 2*self.N*self.L-1), dtype=np.complex64)
        for i in range(1, 2*self.L):
            D[i - 1, i * self.N - 1] = 1

        D = sp.sparse.csr_matrix(D)
        # Calculate M^2 filter cross correlations
        cross_correlations = np.zeros(
            (self.M**2, 2*self.N-1), dtype=np.complex64)
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
        column_padding = np.zeros(
            2*self.N*self.L - 2*self.N, dtype=np.complex64)
        row_padding = np.zeros(self.N*self.L*2-2, dtype=np.complex64)
        for i in range(0, self.M**2):
            column = np.concatenate((cross_correlations[i, :], column_padding))
            row = np.insert(row_padding, 0, cross_correlations[i, 0])
            Rcc = sp.sparse.csr_matrix(sp.linalg.toeplitz(column, row))
            R[i*(2*self.L-1):((i+1)*(2*self.L-1)), :] = D.dot(Rcc).toarray()
        return R[:, self.N - 1:-(self.N)]

    def get_filename(self):
        return (cg.CACHE_DIR + "wessel_cache_" + str(self.N) + str(self.L) + str(self.M))
