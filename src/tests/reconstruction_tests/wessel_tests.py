import unittest
import scipy as sp
import scipy.io
import scipy.linalg
import spectral.core as sc
import numpy as np


class WesselTests(unittest.TestCase):
    def setUp(self):
        self.ref = sp.io.loadmat("./tests/reconstruction_tests/wessel_tests")
        self.wes = sc.reconstruction.Wessel(self.ref['L'][0][0], self.ref['C'], cache=False)
        self.L = self.ref['L'][0][0]
        self.K = self.ref['K'][0][0]
        self.N = self.ref['N']
        self.y = self.sample(self.ref['C'], self.ref['x'])

    def tearDown(self):
        pass

    def test_full_column_rank(self):
        shape = self.wes.R.shape
        rank = np.linalg.matrix_rank(self.wes.R)
        self.assertEqual(min(shape), rank)

    def test_correct_R(self):
        np.testing.assert_array_almost_equal(self.wes.get_Rpinv(), self.ref['R_inv'])

    def test_correct_output(self):
        psd1 = np.absolute(self.ref['PSD_est']).ravel()
        psd2 = np.absolute(np.fft.fft(self.wes.reconstruct(self.y).ravel()))
        np.testing.assert_array_almost_equal(psd1, psd2)

    def sample(self, C, x):
        offset = x.shape[0] % self.N
        if offset != 0:
            x = x[:-offset]
        y = np.dot(C, x.transpose().reshape((self.N, -1), order='F'))
        return y

    def test_cross_correlation_matrix(self):
        ry = self.wes.cross_correlation_signals(self.y).ravel()
        ry_ref = self.ref['ry'].ravel()
        np.testing.assert_array_almost_equal(ry, ry_ref)
