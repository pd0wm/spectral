import unittest
import spectral.core as sc
import numpy as np


class TestHelperfunctions(unittest.TestCase):

    def test_signal_power(self):
        signal = np.linspace(0, 4, 5)
        power = sc.signal_power(signal)
        power_ref = 6.0
        self.assertEqual(power, power_ref)

    def test_hermitian(self):
        matrix = np.array([[1 + 1j, 0 + 5j],
                           [2 - 3j, 4 + 1j]])
        matrix_ref = np.array([[1 - 1j, 2 + 3j],
                              [0 - 5j, 4 - 1j]])
        matrix_H = sc.hermitian(matrix)
        np.testing.assert_array_equal(matrix_H, matrix_ref)

    def test_fft(self):
        fft_ref = np.array([5.55655774595920, 6.04640121289538, 7.27754296745640,
                            10.1731127625259, 19.5220604308632, 55,
                            19.5220604308632, 10.1731127625259, 7.27754296745640,
                            6.04640121289538, 5.55655774595920])
        signal = np.linspace(0, 10, 11)
        fft = sc.fft(signal)
        np.testing.assert_array_almost_equal(fft, fft_ref)

    def test_convert_db(self):
        ref_db = -6.0
        decimal = 10 ** float(ref_db / 10.0)
        db = sc.convert_db(decimal)
        self.assertEqual(db, ref_db)

    def test_invert_db(self):
        ref_decimal = 200
        db = sc.convert_db(ref_decimal)
        dec = sc.invert_db(db)
        self.assertAlmostEqual(dec, ref_decimal)

    def test_psd(self):
        inp = np.linspace(0, 4, 5)
        psd = sc.psd(inp)
        psd_ref = np.array([0.220733041680088, 1.33333333333333, 1.15459744242736,
                           12.9338644007473, 27.3333333333333, 12.9338644007473,
                           1.15459744242736, 1.33333333333333, 0.220733041680088])
        np.testing.assert_array_almost_equal(psd, psd_ref)

    def test_remove_bias(self):
        begin = np.linspace(1, 4, 4)
        end = np.linspace(1, 3, 3)
        triang = np.zeros(len(begin) + len(end))
        triang[:len(begin)] = begin
        triang[-len(end):] = end[::-1]
        output = sc.remove_bias(triang)
        ref = np.ones(len(triang))
        np.testing.assert_array_equal(output, ref)

    def test_add_bias(self):
        ref_begin = np.linspace(1, 4, 4)
        ref_end = np.linspace(1, 3, 3)
        ref = np.zeros(len(ref_begin) + len(ref_end))
        ref[:len(ref_begin)] = ref_begin
        ref[-len(ref_end):] = ref_end[::-1]
        inp = np.ones(len(ref))
        out = sc.add_bias(inp)
        np.testing.assert_array_equal(out, ref)

    def test_cross_correlate(self):
        inp1 = np.linspace(1, 4, 4)
        inp2 = np.linspace(4, 7, 4)
        out = sc.cross_correlate(inp1, inp2, maxlag=2, unbiased=False)
        ref = np.array([20, 38, 60, 47, 32])
        np.testing.assert_array_almost_equal(out, ref)

    def test_auto_correlation(self):
        inp = np.linspace(1, 5, 5)
        out = sc.auto_correlation(inp, maxlag=1)
        ref = np.array([10, 11, 10], dtype=np.float64)
        np.testing.assert_array_almost_equal(out, ref)
