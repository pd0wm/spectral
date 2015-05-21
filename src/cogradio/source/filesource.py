import numpy as np
import os


class File(object):

    """Signal coming from a file"""

    def __init__(self, filename, offset=0, dtype=np.complex64):
        self.data_type = dtype
        self.item_size = np.dtype(dtype).itemsize
        self.data_file = open(filename, 'rb')
        self.offset = offset

        # Calculate file length
        self.data_file.seek(0, os.SEEK_END)
        self.length = self.data_file.tell()

    def generate(self, no_samples):
        self.data_file.seek((self.offset * self.item_size) % self.length)
        samples = np.fromfile(self.data_file, self.data_type, count=no_samples)
        self.offset += no_samples
        return samples
