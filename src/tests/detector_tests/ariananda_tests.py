import unittest
import scipy.io
import scipy as sp
import spectral_core as sc
import numpy as np


class ArianandaTests(unittest.TestCase):
    def setUp(self):
        self.ref = sp.io.loadmat("./tests/detector_tests/ariananda.mat")
        L = self.ref['L'][0, 0]
        K = self.ref['K'][0, 0]
        # window_length = self.
        Pfa = self.ref['pfa'][0, 0]
        C = self.ref['C']
        R_pinv = self.ref['R_inv']
        filter_correlations = self.ref['rc']
        self.detect = sc.detection.Ariananda(L, K, C, R_pinv, filter_correlations, 20, Pfa)

    def test_sigma(self):
        inp = self.ref['rx_est']
        psd = sc.fft(inp.ravel())
        sigma = self.detect.estimate_sigma(psd)
        sigma_ref = self.ref['sigma_est'][0][0]
        np.testing.assert_almost_equal(sigma, sigma_ref)

    def test_ryexp(self):
        sigma = self.ref['sigma_est']
        ry_exp = self.detect.generate_ryexp(sigma)
        ry_exp_check = self.ref['ryexp'].ravel()
        print ry_exp
        np.testing.assert_array_almost_equal(ry_exp, ry_exp_check)

    def test_generate_cry(self):
        sigma = self.ref['sigma_est']
        Cry = self.detect.generate_Cry(sigma)
        Cry_ref = self.ref['Cry']
        np.testing.assert_array_almost_equal(Cry, Cry_ref)

    def test_generate_csx(self):
        Cry = self.ref['Cry']
        Csx = self.detect.generate_Csx(Cry)
        Csx_ref = self.ref['Csx']
        np.testing.assert_array_almost_equal(Csx, Csx_ref)

    def test_calc_threshold(self):
        Csx = self.ref['Csx']
        psd = self.ref['psd_exp'].ravel()
        sigma = self.ref['sigma_est']
        thresh = self.detect.calc_threshold(Csx, psd, sigma).ravel()
        thresh_check = self.ref['gamma'].ravel()
        np.testing.assert_array_almost_equal(thresh, thresh_check)

    def test_check_output(self):
        ref_output = self.ref['detected'].ravel()
        inp = self.ref['rx_est'].ravel()
        output = self.detect.detect(inp)
        out_num = np.zeros(len(output))
        for i, j in enumerate(output):
            if j:
                out_num[i] = 1
            else:
                out_num[i] = 0
        print out_num - ref_output
        np.testing.assert_array_equal(output, ref_output)
