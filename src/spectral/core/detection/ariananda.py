from .detector import Detector
import numpy as np
import spectral as spec
import scipy as sp


class Ariananda(Detector):

    "Estimated Noise Power Energy Detector"

    def __init__(self, L, K, C, R_pinv, filter_correlations, window_length=50, Pfa=0.1):
        self.L = L
        self.K = K

        self.Pfa = Pfa
        self.window_length = window_length

        self.C = C
        self.M = self.C.shape[0]
        self.N = self.C.shape[1]
        self.rc = filter_correlations
        self.R_pinv = R_pinv
        R_pinv_h = spec.core.hermitian(R_pinv)
        C_ry = self.generate_Cry()
        C_sx = self.generate_Csx(C_ry, self.R_pinv, R_pinv_h)
        self.triangle = np.diag(np.abs(C_sx))
        self.qinv = sp.stats.norm.isf(self.Pfa)
        ry_exp = self.generate_ryexp()
        self.psd_exp = np.abs(spec.core.fft(self.R_pinv.dot(ry_exp)))

    def detect(self, rx):
        psd = np.abs(spec.core.fft(rx))
        sigma = self.estimate_sigma(psd)
        threshold = self.calc_threshold(sigma)
        return psd > threshold

    def generate_ryexp(self):
        ry_exp = np.zeros((self.M ** 2, 2 * self.L - 1), dtype=np.complex128)
        ry_exp[:, self.L - 1] = self.rc[:, self.N - 1]
        ry_exp = ry_exp.ravel()
        return ry_exp

    def generate_Csx(self, C_ry, R_pinv, R_pinv_h):
        dft = sp.linalg.dft(self.R_pinv.shape[0])
        C_sx = dft.dot(self.R_pinv).dot(C_ry).dot(R_pinv_h).dot(spec.core.hermitian(dft))
        return C_sx

    def generate_Cry(self):
        dim = (2 * self.L - 1) * self.M ** 2
        C_ry = np.zeros((dim, dim), dtype=np.complex128)
        lag_array = np.concatenate((np.arange(self.L), np.arange(-(self.L - 1), 0, 1)))
        for i in range(self.M ** 2):
            for j in range(2 * self.L - 1):
                lag = lag_array[j]
                for k in range(self.M ** 2):
                    a = np.fix(float(i) / self.M) + 1
                    b = np.mod(float(i), self.M) + 1
                    c = np.fix(k / self.M) + 1
                    d = np.mod(k, self.M) + 1
                    rc_comp = self.rc[(a - 1) * self.M + c - 1, self.N - 1]
                    rc_comp_conj = np.conj(self.rc[(b - 1) * self.M + d - 1, self.N - 1])
                    scaling_factor = (self.L * self.K - np.abs(lag))
                    index_i = i * (2 * self.L - 1) + j
                    index_j = k * (2 * self.L - 1) + j
                    C_ry[index_i, index_j] = rc_comp * rc_comp_conj / scaling_factor
        return C_ry

    def estimate_sigma(self, psd):
        noise_estimate = np.zeros(len(psd))
        # Sliding window over frequency bins
        for i in range(0, len(psd)):
            kidx = max(0, i - self.window_length)
            gidx = min(len(psd), i + 1 + self.window_length)
            noise_estimate[i] = np.mean(psd[kidx:gidx])
        return np.sqrt(min(noise_estimate))  # /len(psd)

    def calc_threshold(self, sigma):
        offset = self.psd_exp * sigma ** 2
        threshold = self.qinv * np.sqrt(sigma ** 4 * self.triangle) + offset
        return threshold

    def parse_options(self, options):
        for key, value in options.items():
            if key == "window_length":
                self.window_length = options["window_length"]
            elif key == "Pfa":
                self.Pfa = options["Pfa"]
