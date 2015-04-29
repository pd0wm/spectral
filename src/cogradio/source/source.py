class Source(object):

    """Source object for spectrum sensing"""

    def __init__(self, frequencies, SNR):
        self.frequencies = frequencies
        self.SNR = SNR

    def generate(self, samp_freq, duration):
        raise NotImplementedError("Implement this method")
