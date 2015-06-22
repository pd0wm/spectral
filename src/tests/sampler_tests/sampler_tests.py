import unittest
import numpy as np
import spectral.core as sc


class SamplerTests(unittest.TestCase):
    def setUp(self):
        self.sampler = sc.sampling.Sampler()

    def test_sample_not_implemented(self):
        signal = np.zeros(100)

        with self.assertRaises(NotImplementedError):
            self.sampler.sample(signal)

    def test_get_c_not_implemented(self):
        self.assertIsNone(self.sampler.get_C())
