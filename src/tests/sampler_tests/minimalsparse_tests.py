import unittest
import numpy as np
import spectral.core as sc


class MinimalSparseRulerTests(unittest.TestCase):
    def setUp(self):
        self.N = 8
        self.sample = sc.sampling.MinimalSparseRuler(self.N)

    def test_sparseruler(self):
        ruler = self.sample.sparseruler(self.N)
        ruler_sol = (0, 1, 2, 3, 7)
        self.assertEqual(ruler, ruler_sol)

    def test_sample(self):
        check_range = 17
        inp = np.linspace(0, check_range - 1, check_range)
        output = self.sample.sample(inp)
        output_ver_1 = np.array([0, 1, 2, 3, 7])
        output_ver_2 = output_ver_1 + self.N
        output_ver = np.array([output_ver_1, output_ver_2], dtype=np.complex128)
        np.testing.assert_array_almost_equal(output, output_ver.T)

    def test_not_in_sparseruler(self):
        with self.assertRaises(NotImplementedError):
            ruler = self.sample.sparseruler(-1)
