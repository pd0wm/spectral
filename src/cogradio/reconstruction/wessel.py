from .reconstructor import Reconstructor
import cogradio as cg
import numpy as np
import scipy as sp


class Wessel(Reconstructor):

    """Implementation of Wessel's adaption of the ariananda algorithm"""

    def __init__(self, N, L, C=None):
        Reconstructor.__init__(self)
        self.L = L
        if C is None:
            self.N = N
            sparseruler = cg.sparseruler(N)
            self.C = cg.build_sparse_ruler_sampling_matrix(sparseruler, N)
        else:
            self.C = C
        # get length of C
        self.M = self.C.shape[0]
        self.N = self.C.shape[1]

        self.R = self.constructR()
        # Force full column rank with slicing
        self.R = self.R[:, (self.N): -(self.N)]
        self.R_pinv = self.calc_pseudoinverse(self.R)

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        ry = self.N * self.cross_correlation_signals(signal)
        ry_stacked = ry.ravel()
        rx = self.R_pinv.dot(ry_stacked)
        return rx

    def constructR(self):
        # Construct "decimation" matrix
        D = np.zeros((2 * self.L - 1, 2 * self.N * self.L - 1), dtype=np.complex64)
        for i in range(1, 2 * self.L):
            D[i - 1, i * self.N - 1] = 1

        D = sp.sparse.csr_matrix(D)
        # Calculate M^2 filter cross correlations
        cross_correlations = np.zeros((self.M ** 2, 2 * self.N - 1),
                                      dtype=np.complex64)
        for i in range(0, self.M):
            for j in range(0, self.M):
                cross_correlations[i * self.M + j, :] = cg.cross_correlate(self.C[i, :],
                                                                           self.C[j, :])
        # Build Rcc toeplitz jetschers, M^2 times
        # containing "toeplitz" filter cross correlation
        Rcc = np.zeros((self.N * self.L * 2 - 1, self.N * self.L * 2 - 1),
                       dtype=np.complex64)

        # Stack all M^2 Rcc matrices
        R = np.zeros((self.M ** 2 * (2 * self.L - 1), 2 * self.N * self.L - 1),
                     dtype=np.complex64)

        # Zero pad cross correlation to create a 2NL-1x2NL-1 matrix

        for i in range(0, self.M ** 2):
            # Calculate Rcicj using Toeplitz
            row = np.zeros(2 * self.N * self.L - 1, dtype=np.complex64)
            column = np.zeros(2 * self.N * self.L - 1, dtype=np.complex64)
            row[0] = cross_correlations[i, 0]
            column[:len(cross_correlations[i, :])] = cross_correlations[i, :]
            Rcc = sp.sparse.csr_matrix(sp.linalg.toeplitz(column, row))

            # Place in R
            R[i * (2 * self.L - 1):((i + 1) * (2 * self.L - 1)), :] = D.dot(Rcc).toarray()
        return R


