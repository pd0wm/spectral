from nose.tools import *
import numpy as np
import cogradio as cg


def sinusoidal_snr_test():
    snr = 20
    signal = cg.source.Sinusoidal([10e3], SNR=snr).generate(250e3, 1)
    print cg.convert_db(snr_meas)
    assert_equal(snr_meas, snr)
