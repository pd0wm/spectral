#!/usr/bin/env python2


class sampler(object):

    """A parent class for sampling methods"""

    def __init__(self, frequency, sparsity, sample_length):
        """TODO: to be defined1.

        :frequency: TODO
        :sparsity: TODO
        :sample_length: TODO

        """
        self._frequency = frequency
        self._sparsity = sparsity
        self._sample_length = sample_length

    def sample(self, signal):
        pass
