import numpy as np
import os

class File(object):

    def __init__(self, filename, offset=0, dtype=np.complex64):
        self._dtype = dtype
        self._itemsize = np.dtype(dtype).itemsize
        self._file = open(filename, 'rb')
        self._offset = offset

        # Calculate file length
        self._file.seek(0, os.SEEK_END)
        self._length = self._file.tell()

    def generate(self, no_samples):
        self._file.seek((self._offset * self._itemsize) % self._length)
        samples = np.fromfile(self._file, self._dtype, count=no_samples)
        self._offset += no_samples
        return samples
