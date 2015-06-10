from .detector import Detector
import numpy as np
import cogradio as cg
import scipy.stats as stats


class noise_power(Detector):

    "Estimated Noise Power Energy Detector"

    def __init__(self, Pfa=0.1, window_length=50, num_bins=150):
        self.Pfa = Pfa
        self.window_length = window_length
        self.num_bins = num_bins

    def detect(self, rx):
        psd = abs(cg.fft(rx))
        # create array for power in bin
        power = np.zeros(self.num_bins)
        stepsize = np.floor(len(psd) / self.num_bins)
        # calculate threshold for energy (time domain)
        self.threshold = self.calc_threshold(psd)

        # calculate variance of noise
        noise_variance = self.calc_noise_variance(psd)
        noise_level = noise_variance*len(psd)/2
        # simulate noise in the other numbins-1 bands
        additive_noise = (len(psd)-stepsize)*noise_level

        for i in range(0, self.num_bins):
            power[i] = (
                np.sum(psd[stepsize * (i - 1) + 1:stepsize * i - 1]) +
                additive_noise)/len(psd)

        return power > self.threshold

    def parse_options(self, options):
        for key, value in options.items():
            if key == "num_bins":
                self.num_bins = options["num_bins"]
            elif key == "window_length":
                self.window_length = options["window_length"]
            elif key == "Pfa":
                self.Pfa = options["Pfa"]

    def calc_noise_variance(self, psd):
        noise_estimate = np.zeros(len(psd))

        # Sliding window over frequency bins
        for i in range(0, len(psd)):
            kidx = max(0, i - self.window_length)
            gidx = min(len(psd) - 1, i + self.window_length)
            noise_estimate[i] = np.mean(psd[kidx: gidx])

        return 2*min(noise_estimate)/len(psd)

    def calc_threshold(self, psd):
        # calculate the length of the TIME DOMAIN signal
        N = (len(psd)+1)/2
        noise_variance = self.calc_noise_variance(psd)
        threshold = (stats.norm.isf(self.Pfa)*np.sqrt(N)+N)*noise_variance
        return threshold
