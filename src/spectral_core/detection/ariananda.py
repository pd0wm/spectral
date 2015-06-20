from .detector import Detector
import numpy as np
import spectral_core as sc
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
        self.R_pinv_t = sc.hermitian(R_pinv)

    def detect(self, rx):
        psd = abs(sc.fft(rx))
        sigma = self.estimate_sigma(psd)

        ry_exp = self.generate_ryexp(sigma)
        psd_exp = np.abs(sc.fft(self.R_pinv.dot(ry_exp)))

        C_ry = self.generate_Cry(sigma)
        C_sx = self.generate_Csx(C_ry)

        threshold = self.calc_threshold(C_sx, psd_exp, sigma)
        return psd > threshold

    def generate_ryexp(self, sigma):
        ry_exp = np.zeros((self.M ** 2, 2 * self.L - 1), dtype=np.complex128)
        ry_exp[:, self.L - 1] = self.rc[:, self.N - 1]
        ry_exp = ry_exp.ravel()
        return ry_exp

    def generate_Csx(self, C_ry):
        dft = sp.linalg.dft(self.R_pinv.shape[0])
        C_sx = dft.dot(self.R_pinv).dot(C_ry).dot(self.R_pinv_t).dot(sc.hermitian(dft))
        return C_sx

    def generate_Cry(self, sigma):
        dim = (2*self.L-1)*self.M**2
        C_ry = np.zeros((dim, dim), dtype=np.complex128)
        lag_array = np.concatenate((np.arange(self.L), np.arange(-(self.L-1), 0, 1)))
        for i in range(self.M**2):
            for j in range(2*self.L-1):
                lag = lag_array[j]
                for k in range(self.M**2):
                    a = np.floor(i/self.M)
                    b = np.mod(i, self.M)
                    c = np.floor(k/self.M)
                    d = np.mod(k, self.M)
                    C_ry[i*(2*self.L-1) + j, k*(2*self.L-1) + j] = sigma**4 * self.rc[a*self.M + c, self.N-1] * np.conj(self.rc[b*self.M + d, self.N-1]) / (self.L*self.K - np.abs(lag))
        return C_ry

    def estimate_sigma(self, psd):
        noise_estimate = np.zeros(len(psd))

        # Sliding window over frequency bins
        for i in range(0, len(psd)):
            kidx = max(0, i - self.window_length)
            gidx = min(len(psd), i + 1 + self.window_length)
            noise_estimate[i] = np.mean(psd[kidx:gidx])

        return np.sqrt(min(noise_estimate))  # /len(psd)

    def calc_threshold(self, C_sx, psd_exp, sigma):
        offset = psd_exp*sigma ** 2
        threshold = sp.stats.norm.isf(self.Pfa) * np.sqrt(sigma ** 4 * np.diag(np.abs(C_sx))) + offset

        return threshold

    def parse_options(self, options):
        for key, value in options.items():
            if key == "window_length":
                self.window_length = options["window_length"]
            elif key == "Pfa":
                self.Pfa = options["Pfa"]
