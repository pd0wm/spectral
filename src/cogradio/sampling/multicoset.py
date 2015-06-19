import numpy as np
from .sampling import Sampler


class MultiCoset(Sampler):

    """Multi coset sampler implementation. Class that converts uniformly sampled signals
    into aperiodically sampled ones.

    Args:
        intervals: Intervals that the multi-coset sampler samples at.
        N: The downsampling factor.
        M: Number of devices."""

    def __init__(self, intervals, N, M):

        super(MultiCoset, self).__init__()
        self.C = self.build_sampling_matrix(intervals, N, M)
        self.N = self.C.shape[1]
        self.M = self.C.shape[0]

    def sample(self, signal):
        """ Takes a uniformly sampled signal and turns it into
        an aperiodically sampled one.

        Args:
            signal: Uniformly sampled signal. If it is not a multiple of the downsampling factor the end will be cut off to match it.
        Returns:
            Aperiodically sampled signal as defined by the set of intervals.
        """
        length = signal.shape[0]
        offset = length % self.N
        if offset != 0:
            signal = signal[:-offset]
        signal = np.reshape(signal.T, (self.N, -1), order='F')
        output = np.dot(self.C, signal)
        return output

    def build_sampling_matrix(self, intervals, N, M):
        """ Builds the sampling matrix from a set of intervals

        Args:
            intervals: Set of intervals
            N: downsampling factor
            M: number of devices

        Returns:
            (MxN) sampling matrix
        """
        C = np.zeros((M, N), np.complex128)
        for i, j in enumerate(intervals):
            C[i, j] = 1
        return C
