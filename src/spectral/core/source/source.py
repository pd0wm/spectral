class Source(object):

    """
    Base class of a source. Defines the abstract function
    for signal generation and option parsing

    Agrs:
        samp_fre: Sample frequency
    """

    def __init__(self, samp_freq):
        self.samp_freq = float(samp_freq)

    def generate(self, no_samples):
        """
        Abstract function to generate samples.

        Args:
            no_samples: Number of samples to generate

        Returns:
            Generated samples
        """
        raise NotImplementedError("Implement this method.")

    def parse_options(self, options):
        """
        Funtion to parse options from the client.

        Args:
           options: Dictionary with options
        """
        pass
