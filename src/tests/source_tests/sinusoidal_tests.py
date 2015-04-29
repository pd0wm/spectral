from nose.tools import *
from cogradio.source import Sinusoidal
import numpy as np


def sinusoidal_snr_test():
    snr = 20
    signal = Sinusoidal([10e3], SNR=snr).generate(250e3, 1)
    snr_meas = np.mean(signal) / np.sqrt(np.var(signal))
    print snr_meas
    assert_equal(snr_meas, snr)
