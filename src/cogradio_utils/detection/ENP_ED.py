from .detector import Detector
import numpy as np
import cogradio_utils as cg
import scipy.stats as stats


class ENP_ED(Detector):

    "Estimated Nose Power Energy Detector"

    def __init__(self, Pfa):
        self.Pfa = Pfa
        # TODO: analyze influence of window length and number of bins
        self.win_length = 50
        self.numbins = 20

    def detect(self, rx):
        length = (len(rx)-1)/2
        # Normalize autocorrelation
        autocorr = rx / max(abs(rx))
        # Normalize PSD
        psd = cg.fft(autocorr)/(2*length)

        # Create a noise level estimate
        noise_estimate = np.zeros(length)

        # Sliding window over frequency bins
        for i in range(0, length):
            kidx = max(0, i-self.win_length)
            gidx = min(length-1, i+self.win_length)
            noise_estimate[i] = np.mean(psd[kidx: gidx])

        # Minimum level should equal noise (signal only adds up to PSD)
        noise_level = min(abs(noise_estimate))
        stepsize = np.floor(len(psd)/self.numbins)
        threshold = (stats.norm.isf(self.Pfa)+np.sqrt(stepsize)) * \
            np.sqrt(stepsize)*2*noise_level

        power = np.zeros(self.numbins)
        for i in range(0, self.numbins):
            power[i] = np.sum(psd[stepsize*(i-1)+1:stepsize*i-1]**2)
        return power > threshold
