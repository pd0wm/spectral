class Sampler(object):

    """A parent class for sampling methods"""

    def __init__(self):
        pass

    def sample(self, signal):
        raise NotImplementedError("Implement this method")
