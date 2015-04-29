from nose.tools import *
from cogradio.source import Sinusoidal


def check_SNRLESS_signal():
    signal = Sinusoidal([10, 20])
    assert_equal(signal.generate(50, 0.1), TEST_CASE_SNR_LESS)

