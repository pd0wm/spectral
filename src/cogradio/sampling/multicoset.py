import numpy as np
import cogradio as cg
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation"""

    def __init__(self, decimation, mode="msr"):
        Sampler.__init__(self)
        self.decimation = decimation
        self.mode = mode

    def sample(self, signal):
        if self.mode == "msr":
            C = self.get_C()
            length = int(np.floor(len(signal) / self.decimation))
            y = np.zeros((len(C[0:]), length))

            for i in np.arange(0, len(signal), self.decimation):
                y[:, i / self.decimation] = np.dot(np.fliplr(C), signal[i:(i + self.decimation)])

            return y
        else:
            raise NotImplementedError("Unsupported mode: " + self.mode)

    def get_C(self):
        S = self.RULERS[self.decimation - 1]
        M = len(S)
        C = np.zeros((M, self.decimation))

        for i in range(0, M):
            C[i, S[i]] = 1

        return C

    RULERS = {
        1: (0, 1),
        2: (0, 1, 2),
        3: (0, 1, 3),
        4: (0, 1, 2, 4),
        5: (0, 1, 2, 5),
        6: (0, 1, 4, 6),
        7: (0, 1, 2, 3, 7),
        8: (0, 1, 2, 5, 8),
        9: (0, 1, 2, 6, 9),
        10: (0, 1, 2, 3, 6, 10),
        11: (0, 1, 2, 3, 7, 11),
        12: (0, 1, 2, 3, 8, 12),
        13: (0, 1, 2, 6, 10, 13),
        14: (0, 1, 2, 3, 4, 9, 14),
        15: (0, 1, 3, 6, 10, 14, 15),
        16: (0, 1, 2, 3, 8, 12, 16),
        17: (0, 1, 2, 3, 8, 13, 17),
        18: (0, 1, 4, 7, 10, 13, 16, 18),
        19: (0, 1, 2, 3, 4, 9, 14, 19),
        23: (0, 1, 2, 11, 15, 18, 21, 23),
        29: (0, 1, 2, 14, 18, 21, 24, 27, 29)
    }
