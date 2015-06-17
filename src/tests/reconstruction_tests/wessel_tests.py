import unittest
import scipy as sp
import scipy.io
import scipy.linalg
import cogradio as cg
import numpy as np


def herm(a):
    return np.transpose(np.conjugate(a))


class Wessel_test(unittest.TestCase):
    MAX_ERROR = 10 ** (-12)

    def setUp(self):
        self.dony = sp.io.loadmat("./tests/reconstruction_tests/wessel_tests")
        self.wes = cg.reconstruction.Wessel(self.dony['L'][0][0], self.dony['C'])
        self.sampler = cg.sampling.MultiCoset(0, C=self.dony['C'])
        self.L = self.dony['L'][0][0]
        self.K = 1984
        y = self.sample(self.dony['C'], self.dony['x'])
        self.ry = self.wes.cross_correlation_signals(y)

    def tearDown(self):
        pass

    def test_full_column_rank(self):
        shape = self.wes.R.shape
        rank = np.linalg.matrix_rank(self.wes.R)
        self.assertEqual(min(shape), rank)

    def test_correct_R(self):
        error = sp.linalg.norm(self.wes.R_pinv - self.dony['R_inv'])
        self.assertLess(error, self.MAX_ERROR)

    def test_correct_output(self):
        psd1 = np.absolute(self.dony['PSD_ruler']).T
        psd2 = np.absolute(np.fft.fft(self.wes.R_pinv.dot(self.ry).T))

        self.assertLess(np.linalg.norm(psd1 - psd2), self.MAX_ERROR)

    def sample(self, C, x):
        y = np.dot(C, x.transpose().reshape((self.dony['N'], self.L * self.K), order='F'))
        return y

    def test_cross_correlation_matrix(self):
        error = sp.linalg.norm(self.dony['ry'] - self.ry)
        self.assertLess(error, self.MAX_ERROR)
