from .source import Source
import numpy as np
import os


class File(Source):

    """
    Signal coming from a prerecorded file.

    Args:
        filename: Filename of the source file
        offset: Point where the reading starts
        dtype: Datatype of the recorded file

    """

    def __init__(self, filename, offset=0, dtype=np.complex64):
        self.data_type = dtype
        self.item_size = np.dtype(dtype).itemsize
        self.data_file = open(filename, 'rb')
        self.offset = offset

        # Calculate file length
        self.data_file.seek(0, os.SEEK_END)
        self.length = self.data_file.tell()

    def generate(self, no_samples):
        """
        Generator that reads the signal from the file. Increments the offset
        variable to the next block of samples. Wraps around on file end.

        Args:
            no_samples: Number of samples to read

        Returns:
            Samples that are read from the file

        """
        self.data_file.seek((self.offset * self.item_size) % self.length)
        samples = np.fromfile(self.data_file, self.data_type, count=no_samples)
        self.offset += len(samples)

        if len(samples) != no_samples:
            diff = no_samples - len(samples)
            self.data_file.seek((self.offset * self.item_size) % self.length)
            samples = np.concatenate([samples, np.fromfile(self.data_file, self.data_type, count=diff)])

            self.offset += diff

        return samples
