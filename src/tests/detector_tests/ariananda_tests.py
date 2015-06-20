import unittest
import scipy.io
import scipy as sp
import spectral_core as sc


class ArianandaTests(unittest.TestCase):
    def setUp(self):
        self.ref = sp.io.loadmat("./tests/detector_tests/ariananda.mat")
        L = self.ref['L'][0, 0]
        K = self.ref['K'][0, 0]
        # window_length = self.
        Pfa = self.ref['pfa'][0, 0]
        C = self.ref['C']
        R_pinv = self.ref['R_inv']
        print L, K, Pfa
        filter_correlations = self.ref['rc']
        self.detect = sc.detection.Ariananda(L, K, C, R_pinv, filter_correlations)
        self.detect.parse_options({"Pfa": Pfa})

    def testFail(self):
        print self.ref['D']
        assert(False)
