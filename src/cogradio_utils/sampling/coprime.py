import numpy as np
import cogradio_utils as cg
from .sampling import Sampler


class Coprime(Sampler):

    """Coprime coset sampler implementation"""

    def __init__(self, N, mode="cps"):
        Sampler.__init__(self)
        self.N = N
        self.mode = mode
        sparseruler = cg.sparseruler(N)
        self.C = cg.build_C(sparseruler, N)
        self.M = len(sparseruler)
        self.D1 = 3; # sample rate of device 1
        self.D2 = 5; # sample rate of device 2

    def sample(self, signal):
        if self.mode == "cps":
            return self.__cps_sample(signal)
        else:
            raise NotImplementedError("Unsupported mode: " + self.mode)

    def generateC(self):
        C = np.zeros((self.D1+self.D2, self.D1*self.D2))
        for i in range(self.D1):
            C[i,i*self.D2] = 1
        for i in range(self.D2):
             C[i+self.D1,i*self.D1] = 1
        # print(C)
        return(C)

    def __cps_sample(self, signal):
        length = int(np.floor(len(signal) /(self.D1*self.D2)))
        y = np.zeros((self.D1+self.D2, length))
        for l in range((length)):
            for i in range(self.D1):
                y[i,l] = signal[i*self.D2+l*self.D1*self.D2]
            for i in range(self.D2):
                y[i+self.D1,l] = signal[i*self.D1+l*self.D1*self.D2]

        

        # length = int(np.floor(len(signal) / self.N))
        # tmp = length * self.N
        # y = np.zeros((self.M, length))
        # for i in np.arange(0, tmp, self.N):
        #     y[:, i / self.N] = np.dot(np.fliplr(self.C),
        #                               signal[i:(i + self.N)])
        # print(y)
        # print(y.shape)
        # print(y)
        return(y)
