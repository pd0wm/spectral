import unittest
import numpy as np
import spectral.core as sc


class CoprimeTests(unittest.TestCase):
    def setUp(self):
        self.a = 3
        self.b = 5
        self.sample = sc.sampling.Coprime(self.a, self.b)

    def test_coprime_multiples_pos(self):
        coprime_mults = [0, 3, 5, 6, 9, 10, 12]
        self.assertEqual(coprime_mults, list(self.sample.coprime_multiples(self.a, self.b)))

    def test_sample_method(self):
        range_check = 33
        inp = np.linspace(0, range_check - 1, range_check)
        out = self.sample.sample(inp)
        output_check_1 = np.array([0, 3, 5, 6, 9, 10, 12])
        output_check_2 = output_check_1 + (self.a * self.b)
        ver = np.zeros((len(output_check_1), 2))
        ver[:, 0] = output_check_1
        ver[:, 1] = output_check_2
        np.testing.assert_array_equal(ver, out)
