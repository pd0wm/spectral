import unittest
import numpy as np
import spectral.core as sc
import tempfile


class FileSourceTests(unittest.TestCase):
    def setUp(self):
        self.f = tempfile.NamedTemporaryFile(delete=True)
        self.dtype = np.complex64

        self.test_data = np.linspace(1, 100, 100, dtype=self.dtype)
        self.test_data.tofile(self.f.name)


    def zero_offset_test(self):
        self.source = sc.source.File(self.f.name, dtype=self.dtype)

        self.assertTrue(np.alltrue(np.linspace(1, 10, 10, dtype=self.dtype) == self.source.generate(10)))


    def continue_test(self):
        self.source = sc.source.File(self.f.name, dtype=self.dtype)

        self.source.generate(10)
        self.assertTrue(np.alltrue(np.linspace(11, 20, 10, dtype=self.dtype) == self.source.generate(10)))


    def non_zero_offset_test(self):
        self.source = sc.source.File(self.f.name, offset=10, dtype=self.dtype)

        self.assertTrue(np.alltrue(np.linspace(11, 20, 10, dtype=self.dtype) == self.source.generate(10)))

    def overflow_test(self):
        self.source = sc.source.File(self.f.name, offset=95, dtype=self.dtype)

        expected = np.concatenate([np.linspace(96, 100, 5, dtype=self.dtype), np.linspace(1, 5, 5, dtype=self.dtype)])
        samples = self.source.generate(10)

        self.assertTrue(np.alltrue(expected == samples))
