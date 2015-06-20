from .source import Source
import numpy as np
try:
    from gnuradio import uhd
except ImportError:
    class uhd:
        def usrp_source(*args, **kwargs):
            raise RuntimeError("UHD lib not installed")


class UsrpN210(Source):

    """Implementation of UsrpN210 driver"""

    def __init__(self, addr, samp_freq=25e6, center_freq=2.4e9, lo_offset=12.5e6, gain=10, sample_format='fc32'):
        self.samp_freq = samp_freq
        self.center_freq = 0
        self.lo_offset = lo_offset
        self.gain = gain
        self.window = [0]
        self.uhd = uhd.usrp_source("addr=" + addr,
                                   uhd.stream_args(
                                       cpu_format=sample_format,
                                       channels=range(1),
                                   ))
        self.uhd.set_samp_rate(self.samp_freq)
        self.uhd.set_antenna("TX/RX", 0)
        self.uhd.set_bandwidth(self.samp_freq / 2, 0)
        self.set_frequency(center_freq)
        self.set_gain(gain)

    def set_frequency(self, frequency):
        if self.center_freq != frequency:
            print "Tuning to", frequency / 1e9, "GHz"
            self.center_freq = frequency
            self.uhd.set_center_freq(uhd.tune_request(frequency, self.lo_offset), 0)

    def set_gain(self, gain):
        if self.gain != gain:
            self.gain = gain
            self.uhd.set_gain(gain, 0)

    def generate(self, num_samples):
        samples = self.uhd.finite_acquisition(num_samples + 1000)[1000:]
        samples -= np.mean(samples)

        if len(samples) != num_samples:
            raise RuntimeError("Number of samples from USRP incorrect")

        return np.array(samples)

    def parse_options(self, options):
        for key, value in options.items():
            if key == 'antenna_gain':
                self.set_gain(value)
            if key == 'center_freq':
                self.set_frequency(value * 1e9)