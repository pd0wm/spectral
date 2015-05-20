import numpy as np


class FromFile(source):

    """Docstring for FromFile. """

    def __init__(self, filename, offset):
        """ Source from data in file """
        self._filename = filename
        self._offset = offset
        self.data = np.loadtxt(self_filename)

    def generate(self, no_samples):
        signal = self.data[self._offset:self._offset + no_samples]
        self._offset += no_samples
        return signal

