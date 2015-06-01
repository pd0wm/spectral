from .detector import Detector
import numpy as np
import cogradio as cg
import scipy.stats as stats


class noise_power(Detector):

    "Estimated Noise Power Energy Detector"

    def __init__(self, threshold, Pfa, window_length, num_bins):
        self.Pfa = Pfa
        self.window_length = window_length
        self.num_bins = num_bins
        self.threshold = threshold

    def detect(self, rx):
        length = (len(rx) - 1) / 2
        psd = cg.fft(rx)
        # create array for power in bins
        power = np.zeros(self.num_bins)

        stepsize = np.floor(len(psd) / self.num_bins)
        self.threshold = self.calc_threshold(psd, rx)
        print self.threshold

        for i in range(0, self.num_bins):
            power[i] = np.sum(psd[stepsize * (i - 1) + 1:stepsize * i - 1])
        return power > self.threshold

    def parse_options(self, options):
        print "Det opt"
        for key, value in options.items():
            if key == "threshold":
                self.threshold = options["threshold"]
            elif key == "num_bins":
                self.num_bins = options["num_bins"]
            elif key == "window_length":
                self.window_length = options["window_length"]

    def calc_threshold(self, psd, rx):
        length = (len(rx) - 1) / 2
        noise_estimate = np.zeros(length)
        # Sliding window over frequency bins
        for i in range(0, length):
            kidx = max(0, i - self.window_length)
            gidx = min(length - 1, i + self.window_length)
            noise_estimate[i] = np.sum(psd[kidx: gidx])

        stepsize = np.floor(len(psd) / self.num_bins)
        noise_level = len(psd)*min(abs(noise_estimate))/stepsize

        return ((stats.norm.isf(self.Pfa) + np.sqrt(stepsize)) *
                np.sqrt(stepsize) * 2 * noise_level)*(stepsize/len(psd))
