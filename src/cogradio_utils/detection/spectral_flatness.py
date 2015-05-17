from .detector import Detector
import numpy as np
import cogradio_utils as cg
import matplotlib.pyplot as plt

class SPFL(Detector):
    """Detection using spectrall flatness Method"""

    def __init__(self):
        Detector.__init__(self)

    def detect(self, rx, binwidth, treshold):
        rx_norm = rx/rx.size
        spectrum_norm = np.abs(np.fft.fftshift(np.fft.fft(rx_norm)))/rx.size
        width = binwidth;
        sstd = np.zeros((spectrum_norm.size,))

        for i in range(spectrum_norm.size):
            iBegin = max(0, int(i-width/2));
            iEnd = min(spectrum_norm.size, i+width/2-1)
            sstd[i] = np.std(spectrum_norm[iBegin:iEnd])

        return  sstd
