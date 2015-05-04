from .reconstructor import Reconstructor
import numpy as np


class CrossCorrelation(Reconstructor):

    """Implementation of ariananda2012 algorithm"""

    def __init__(self, N, M, C, L):
        Reconstructor.__init__(self)
        self.N = N              # Decimation factor
        self.M = M              # Number of channels
        self.C = C              # Sparse ruler matrix
        self.L = L              # Length of input vector
        self.Rc_Pinv = np.linalg.pinv(self.cross_correlation_filters())
        print self.Rc_Pinv.shape


    def reconstruct(self, signal):
        cross_corr_mat = self.cross_correlation_signals(signal)
        y_stacked = cross_corr_mat.ravel(order='F')
        # y_stacked = np.roll(y_stacked, y_stacked.shape[0] / 2 )

        print y_stacked.shape
        print self.L * self.N
        
        np.savetxt("py_ravelsign.tmp", y_stacked, delimiter=',')
        rx = np.dot(self.Rc_Pinv, y_stacked) # Ravel reforms to 1 column
        #rx = np.roll(rx, rx.shape[0] / 2)
        print rx.shape
        return rx

    def cross_correlation_signals(self, signal):
        Ry = np.zeros((self.M**2, 2*self.L + 1))
        for i in range(self.M):
            for j in range(self.M):
                Ry[i * self.M + j] = np.correlate(signal[i, :],
                                                  signal[j, :],
                                                  mode='full')
        np.savetxt("py_ry.tmp", Ry, delimiter=',')

        return Ry

    def cross_correlation_filters(self):
        Rc0 = np.zeros((self.M**2, self.N))
        Rc1 = np.zeros((self.M**2, self.N))
        for i in range(self.M):
            for j in range(self.M):
                rc = np.correlate(self.C[i, :],
                                  self.C[j, :],
                                  mode='full')
                Rc0[i * self.M + j, :] = rc[0:self.N][::-1]
                Rc1[i * self.M + j, :] = np.append(np.array([0]), rc[self.N:2 * (self.N) - 1][::-1])
        Rc = self.block_toeplitz(Rc0, Rc1)
        return Rc

    def block_toeplitz(self, Rc0, Rc1):
        Rc = np.zeros(((2 * self.L + 1)*self.M**2, (2 * self.L + 1) * self.N))
        for i in range((2 * self.L + 1)):
            for j in range((2 * self.L + 1)):
                x = i*self.M**2 # Top left x coordinate
                y = j*self.N    # Top left y coordinate
                if i == j:      # Holy shait pretty multi-dim block indexing mind==blown
                    Rc[x:x+Rc0.shape[0], y:y+Rc0.shape[1]] = Rc0
                elif (i - j) == 1: # Off diagonal entries
                    Rc[x:x+Rc1.shape[0], y:y+Rc1.shape[1]] = Rc1
                elif (j == (2 * self.L) and i == 0): # Right top case
                    print "right top"
                    Rc[x:x+Rc1.shape[0], y:y+Rc1.shape[1]] = Rc1
        return Rc
