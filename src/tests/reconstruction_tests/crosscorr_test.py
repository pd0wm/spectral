import unittest
import scipy as sp
import scipy.io
import numpy as np
import spectral.core as sc


class TestCrossCorr(unittest.TestCase):
    def setUp(self):
        self.ref = sp.io.loadmat("./tests/reconstruction_tests/wessel_tests")
        self.wes = sc.reconstruction.Wessel(self.ref['L'][0][0], self.ref['C'], cache=False)
        self.L = self.ref['L'][0][0]
        self.K = self.ref['K'][0][0]
        self.N = self.ref['N']
        self.y = self.sample(self.ref['C'], self.ref['x'])
        self.recon = sc.reconstruction.CrossCorrelation(self.L, self.ref['C'], cache=False)

    def sample(self, C, x):
        offset = x.shape[0] % self.N
        if offset != 0:
            x = x[:-offset]
        y = np.dot(C, x.transpose().reshape((self.N, -1), order='F'))
        return y

    def test_full_column_rank(self):
        R = self.recon.R
        rank = np.linalg.matrix_rank(R)
        shape = R.shape
        self.assertEqual(min(shape), rank)
