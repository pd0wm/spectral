class Sampler(object):

    """A parent class for sampling methods"""

    def __init__(self, frequency, sparsity, sample_length):
        self._frequency = frequency
        self._sparsity = sparsity
        self._sample_length = sample_length

    def sample(self, signal):
        pass
