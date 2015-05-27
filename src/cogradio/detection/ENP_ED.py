from .detector import Detector
import numpy as np
import cogradio as cg
import scipy.stats as stats


class ENP_ED(Detector):

    "Estimated Nose Power Energy Detector"

    def __init__(self, threshold, Pfa, win_length, numbbins):
        self.Pfa = Pfa
        self.win_length = win_length
        self.numbins = numbbins
        self.threshold = threshold

    def detect(self, rx):
        length = (len(rx) - 1) / 2
        # Normalize autocorrelation
        autocorr = rx / max(abs(rx))
        # Normalize PSD
        psd = cg.fft(autocorr) / (2 * length)
        power = np.zeros(self.numbins)
        stepsize = np.floor(len(psd) / self.numbins)
        for i in range(0, self.numbins):
            power[i] = np.sum(psd[stepsize * (i - 1) + 1:stepsize * i - 1] ** 2)
        return power > self.threshold

    def parse_options(self, options):
        print "Det opt"
        for key, value in options.items():
            if key == "threshold":
                self.threshold = options["threshold"]
            elif key == "numberofbins":
                self.numbbins = options["numberofbins"]
            elif key == "windowlength":
                self.win_length = options["windowlength"]

    def calc_threshold(self, psd, wind_length, rx):
        length = (len(rx) - 1) / 2
        noise_estimate = np.zeros(length)
        # Sliding window over frequency bins
        for i in range(0, length):
            kidx = max(0, i - self.win_length)
            gidx = min(length - 1, i + self.win_length)
            noise_estimate[i] = np.mean(psd[kidx: gidx])

        # Minimum level should equal noise (signal only adds up to PSD)
        noise_level = min(abs(noise_estimate))
        stepsize = np.floor(len(psd) / self.numbins)
        return (stats.norm.isf(self.Pfa) + np.sqrt(stepsize)) * \
            np.sqrt(stepsize) * 2 * noise_level
