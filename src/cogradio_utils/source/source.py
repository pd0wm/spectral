class Source(object):

    """Source parent object for spectrum sensing"""

    def __init__(self, samp_freq):
        self.samp_freq = samp_freq

    def generate(self, no_samples):
        raise NotImplementedError("Implement this method.")
