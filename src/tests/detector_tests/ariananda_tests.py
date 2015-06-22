import unittest
import scipy.io
import scipy as sp
import spectral.core as sc
import numpy as np


class ArianandaTests(unittest.TestCase):
    def setUp(self):
        self.ref = sp.io.loadmat("./tests/detector_tests/ariananda.mat")
        L = int(self.ref['L'][0, 0])
        K = int(self.ref['K'][0, 0])
        Pfa = self.ref['pfa'][0, 0]
        C = self.ref['C']
        R_pinv = self.ref['R_inv']
        filter_correlations = self.ref['rc']
        wl = 20
        self.detect = sc.detection.Ariananda(L, K, C, R_pinv, filter_correlations, wl, Pfa)

    def test_sigma(self):
        inp = self.ref['rx_est']
        psd = sc.fft(inp.ravel())
        sigma = self.detect.estimate_sigma(psd)
        sigma_ref = self.ref['sigma_est'][0, 0]
        np.testing.assert_almost_equal(sigma, sigma_ref)

    def test_ryexp(self):
        ry_exp = self.detect.generate_ryexp()
        ry_exp_check = self.ref['ryexp'].ravel()
        np.testing.assert_array_almost_equal(ry_exp, ry_exp_check)

    def test_generate_cry(self):
        Cry = self.detect.generate_Cry()
        Cry_ref = self.ref['Cry']
        np.testing.assert_array_almost_equal(Cry, Cry_ref)

    def test_generate_csx(self):
        Cry = self.ref['Cry']
        R_pinv = self.ref['R_inv']
        R_pinv_h = sc.hermitian(R_pinv)
        Csx = self.detect.generate_Csx(Cry, R_pinv, R_pinv_h)
        Csx_ref = self.ref['Csx']
        np.testing.assert_array_almost_equal(Csx, Csx_ref)

    def test_calc_threshold(self):
        sigma = self.ref['sigma_est']
        thresh = self.detect.calc_threshold(sigma).ravel()
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
        np.testing.assert_array_equal(output, ref_output)
