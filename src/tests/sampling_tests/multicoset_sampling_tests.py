from cogradio.sampling import MultiCosetSampler
from nose.tools import *


def test_construct():
    mcs = MultiCosetSampler()
    assert_equal(mcs, mcs, msg="Check for type")
