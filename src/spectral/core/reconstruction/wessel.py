from .reconstructor import Reconstructor
import spectral as spec
import numpy as np
import scipy.sparse
import scipy as sp


class Wessel(Reconstructor):

    """Implementation of Wessel's adaption of the ariananda algorithm

    Args:
        L: Maximum lag estimated in the cross-correlation of the cosets.
        C: Sampling matrix used by the sampler used"""

    def __init__(self, L, C, cache=True):
        Reconstructor.__init__(self)
        self.L = L
        self.C = C
        self.M = self.C.shape[0]
        self.N = self.C.shape[1]
        self.R = self.constructR()

        if cache:
            self.R_pinv = self.calc_pseudoinverse(self.R)
        else:
            self.R_pinv = sp.sparse.csr_matrix(sp.linalg.pinv(self.R))

    # Given M decimated channels, try to estimate the PSD
    def reconstruct(self, signal):
        """ Reconstruct method reconstructing the autocorrelation function
        from a a periodically sampled signal

        Args:
            signal: Asymptotically sampled signal.
        Returns:
            reconstructed autocorrelation function.
        """

        ry = self.cross_correlation_signals(signal)
        ry_stacked = ry.ravel()
        rx = self.R_pinv.dot(ry_stacked)
        return rx

    def build_D(self):
        """ Builds the D matrix.

        Returns:
            D matrix
        """
        D = np.zeros((2 * self.L - 1, 2 * self.N * self.L + 2 * self.N - 3), dtype=np.complex128)
        for i in range(1, 2 * self.L):
            D[i - 1, (i + 1) * self.N - 2] = 1
        return D

    def build_rcc(self, cross_correlation):
        """ Builds the Rcc matrix based on the cross_correlation provided.
        Makes use of the nature of the toeplitz generation by entering a modified
        row and column vector and then 'cutting' these to get the matrix required.
        Args:
            cross_correlation: The matrix containing the cross_correlations of the input signal
        Returns:
            Rcc matrix.
        """
        Rcc_dim = 2 * self.N * self.L - 1
        toeplitz_array = np.zeros((Rcc_dim - 1 + len(cross_correlation)), dtype=np.complex128)
        toeplitz_array[:len(cross_correlation)] = cross_correlation
        Rcc = np.tril(sp.linalg.toeplitz(toeplitz_array))[:, :Rcc_dim]
        return Rcc

    def filter_cross_correlation(self):
        cross_correlations = np.zeros((self.M ** 2, 2 * self.N - 1),
                                      dtype=np.complex128)
        for i in range(0, self.M):
            for j in range(0, self.M):
                cross_correlations[i * self.M + j, :] = spec.core.cross_correlate(self.C[i, :],
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
