class Reconstructor(object):

    """Parent class for reconstruction of spectrum sensed signal"""

    def __init__(self):
        pass

    def reconstruct(self, signal):
        raise NotImplementedError("Implement this method.")
