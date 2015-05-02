from .reconstructor import Reconstructor
import numpy as np
from scipy.linalg import toeplitz

class CrossCorrelation(Reconstructor):

    """Implementation of ariananda2012 algorithm"""

    def __init__(self, N, M, C, F_s, chunk_size):
        Reconstructor.__init__(self)
        self.N = N
        self.M = M
        self.C = C
        self.chunk_size = chunk_size
        self.Rc_Pinv = np.linalg.pinv(self.cross_correlation_filters())

    def reconstruct(self, signal):
    	Rx = []
    	Rx = self.Rc_Pinv*self.cross_correlation_signals(signal)


    def cross_correlation_signals(self, signal):
        Ry = np.zeros((self.M**2, 2*self.chunk_size-1))
        for i in range(self.M):
            for j in range(self.M):
                Ry[i * self.M + j] = np.correlate(signal[i, :],
                                                 signal[j, :],
                                                 mode='full')
        return Ry

    def cross_correlation_filters(self):
        Rc0 = Rc1 = np.zeros((self.M**2, self.N))
        Rc = np.zeros(((2*self.chunk_size-1)*self.M**2, self.N*(2*self.chunk_size-1)))
        R_tmp = []
        for i in range(self.M):
            for j in range(self.M):
                R_tmp = np.correlate(self.C[i, :],
                                     self.C[j, :],
                                     mode='full')
                Rc0[:,i*self.M+j] = R_tmp[0:self.N-1]
                Rc1[i*self.M+j] = np.append(np.array([0]), R_tmp[self.N:])#[::-1])
        Rc = toeplitz(Rc0, Rc1)        
        return Rc