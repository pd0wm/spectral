from .reconstructor import Reconstructor
import numpy as np
import scipy as sp


class CrossCorrelation(Reconstructor):

    """Implementation of ariananda2012 algorithm"""

    def __init__(self, L, C, cache=True):
        Reconstructor.__init__(self)
        self.C = C
        self.M = self.C.shape[0]
        self.N = self.C.shape[1]
        self.L = L            # Length of input vector
        self.R = self.cross_correlation_filters()
        if cache:
            self.R_pinv = self.calc_pseudoinverse(self.R)
        else:
            self.R_pinv = sp.sparse.csr_matrix(sp.linalg.pinv(self.R))

    def reconstruct(self, signal):
        cross_corr_mat = self.cross_correlation_signals(signal)
        y_stacked = cross_corr_mat.ravel(order='F')
        rx = self.R_pinv.dot(y_stacked)  # Ravel reforms to 1 column
        return rx

    def cross_correlation_filters(self):
        Rc0 = np.zeros((self.M ** 2, self.N), np.complex128)
        Rc1 = np.zeros((self.M ** 2, self.N), np.complex128)
        for i in range(self.M):
            for j in range(self.M):
                rc = np.correlate(self.C[i, :],
                                  self.C[j, :],
                                  mode='full')
                Rc0[i * self.M + j, :] = rc[0:self.N][::-1]
                Rc1[i * self.M + j, :] = np.append(np.array([0]),
                                                   rc[self.N:2 * self.N - 1][::-1])
        Rc = self.block_toeplitz(Rc0, Rc1)
        return Rc

    def block_toeplitz(self, Rc0, Rc1):
        Rc = np.zeros(((2 * self.L - 1) * self.M ** 2,
                       (2 * self.L - 1) * self.N), np.complex128)
        for i in range((2 * self.L - 1)):
            for j in range((2 * self.L - 1)):
                x = i * self.M ** 2  # Top left x coordinate
                y = j * self.N   # Top left y coordinate
                # Holy shait pretty multi-dim block indexing mind==blown
                if i == j:
                    Rc[x:x + Rc0.shape[0], y:y + Rc0.shape[1]] = Rc0
                elif (i - j) == 1:  # Off diagonal entries
                    Rc[x:x + Rc1.shape[0], y:y + Rc1.shape[1]] = Rc1
                elif (j == (2 * (self.L - 1)) and i == 0):  # Right top case
                    Rc[x:x + Rc1.shape[0], y:y + Rc1.shape[1]] = Rc1
        return Rc
