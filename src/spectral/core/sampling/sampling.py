class Sampler(object):

    """Interface for all samplers in this subpackage"""

    def __init__(self):
        self.C = None

    def sample(self, signal):
        """ Contract that all children implement sample method.

        Raises:
            NotImplementedError: If child does not implement.
        """
        raise NotImplementedError("Implement this method")

    def get_C(self):
        """ Getter function for use in combination with reconstructors and
        other classes that might need the sample matrix.

        Returns:
           sampling matrix.
        """
        return self.C
