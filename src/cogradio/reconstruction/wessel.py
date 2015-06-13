from .reconstructor import Reconstructor
import cogradio as cg
import numpy as np
import scipy as sp
import scipy.io


class Wessel(Reconstructor):

    """Implementation of Wessel's adaption of the ariananda algorithm"""

    def __init__(self, L, C):
        Reconstructor.__init__(self)
        self.L = L
        if C is None:
            sparseruler = cg.sparseruler(N)
            self.C = cg.build_sparse_ruler_sampling_matrix(sparseruler, N)
        else:
            self.C = C

        self.M = self.C.shape[0]
        self.N = self.C.shape[1]

        self.R = self.constructR()
        # Force full column rank with slicing

        self.R_pinv = self.calc_pseudoinverse(self.R)

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        ry = self.cross_correlation_signals(signal)
        ry_stacked = ry.ravel()
        rx = self.R_pinv.dot(ry_stacked)
        return rx

    def build_D(self):
        D = np.zeros((2 * self.L - 1, 2 * self.N * self.L + 2 * self.N - 3), dtype=np.complex128)
        for i in range(1, 2 * self.L):
            D[i - 1, (i + 1) * self.N - 2] = 1
        return D

    def build_rcc(self, cross_correlation):
        Rcc_dim = 2 * self.N * self.L - 1
        toeplitz_array = np.zeros((Rcc_dim - 1+ len(cross_correlation)), dtype=np.complex64)
        toeplitz_array[:len(cross_correlation)] = cross_correlation
        Rcc = np.tril(sp.linalg.toeplitz(toeplitz_array))[:, :Rcc_dim]
        return Rcc

    def filter_cross_correlation(self):
        cross_correlations = np.zeros((self.M ** 2, 2 * self.N - 1),
                                      dtype=np.complex128)
        for i in range(0, self.M):
            for j in range(0, self.M):
                cross_correlations[i * self.M + j, :] = cg.cross_correlate(self.C[i, :],
                                                                           self.C[j, :],
                                                                           unbiased=False)
        return cross_correlations

    def constructR(self):
        D = sp.sparse.csr_matrix(self.build_D())

        cross_correlations = self.filter_cross_correlation()

        R = np.zeros((self.M ** 2 * (2 * self.L - 1), 2 * self.N * self.L - 1),
                     dtype=np.complex128)

        for i in range(0, self.M ** 2):
            Rcc = self.build_rcc(cross_correlations[i, :])
            Rcc = sp.sparse.csr_matrix(Rcc)
            R[i * (2 * self.L - 1):((i + 1) * (2 * self.L - 1)), :] = D.dot(Rcc).toarray()
        return R[:, (self.N - 1): -(self.N - 1)]  # Full column rank slicing
