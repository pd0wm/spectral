import unittest
import spectral_core as sc
import numpy as np


class TestHelperfunctions(unittest.TestCase):

    def test_signal_power(self):
        signal = np.linspace(0, 4, 5)
        power = sc.signal_power(signal)
        power_ref = (0**2 + 1 ** 2 + 2 ** 2 + 3 ** 2 + 4 ** 2) / 5
        self.assertEqual(power, power_ref)
 
    def test_hermitian(self):
        matrix = np.array([[1 + 1j, 0 + 5j],
                           [2 - 3j, 4 + 1j]])
        matrix_ref = np.array([[1 - 1j, 2 + 3j],
                              [0 - 5j, 4 - 1j]])
        matrix_H = sc.hermitian(matrix)
        np.testing.assert_array_equal(matrix_H, matrix_ref)
