import unittest
import scipy as sp
import scipy.linalg
import scipy.sparse.linalg
import cogradio as cg
import numpy as np
import matplotlib.pyplot as plt


def herm(a):
    return np.transpose(np.conjugate(a))


class Wessel_test(unittest.TestCase):

    def setUp(self):
        self.dony = sp.io.loadmat("./cogradio/tests/reconstruction_tests/wessel_tests")
        self.wes = cg.reconstruction.Wessel(self.dony['L'][0][0], self.dony['C'])
        self.sampler = cg.sampling.MultiCoset(0, C=self.dony['C'])
        self.L = self.dony['L'][0][0]
        self.K = 1984
        y = self.sample(self.dony['C'], self.dony['x'])
        self.ry = self.matlab_way(y)

    def tearDown(self):
        pass

    def test_full_column_rank(self):
        shape = self.wes.R.shape
        rank = np.linalg.matrix_rank(self.wes.R)
        self.assertEqual(min(shape), rank)

    def test_correct_R(self):
        error = sp.linalg.norm(self.wes.R_pinv - self.dony['R_inv'])
        self.assertLess(error, float(10)**-(12))

    def test_correct_output(self):
        psd1 = np.absolute(self.dony['PSD_ruler']).T
        psd2 = np.absolute(np.fft.fft(self.wes.R_pinv.dot(self.ry).T))

        self.assertLess(np.linalg.norm(psd1 - psd2), 10**-12)

    def sample(self, C, x):
        y = np.dot(C, x.transpose().reshape((self.dony['N'], self.L * self.K), order='F'))
        return y

    def test_cross_correlation_matrix(self):
        error = sp.linalg.norm(self.dony['ry'] - self.ry)
        self.assertLess(error, float(10)**(-12))

    def matlab_way(self, y):
        length = y.shape[1]
        max_lag = self.L - 1
        out = np.zeros((y.shape[0]**2, 2 * self.L - 1), dtype=np.complex128)
        for lag in range(max_lag + 1):
            tmp = np.dot(y[:, lag:(length)], herm(y[:, :(length - lag)]))
            tmp2 = np.reshape(tmp, (-1, 1), order='F') / float(length - lag)
            out[:, lag + max_lag] = tmp2[:, 0]
        for lag in range(max_lag + 1):
            out[:, max_lag - lag] = (np.reshape(
                np.dot(y[:, :length - lag], herm(y[:, lag:length])),
                (-1, 1), order='F')/float(length - lag))[:, 0]

        return out.T.reshape((-1, 1), order='F')

#
#       sp.io.savemat(
#       'tmp', {'x_transp': x.transpose(),
#       'x_resh_transp': x.transpose().reshape((self.dony['N'], self.L * self.K), order='F'),
#       'y_new': y,
#       'C_new': C,
#       'x_new': x})
