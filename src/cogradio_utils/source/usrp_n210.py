from gnuradio import uhd
from scipy import signal


class UsrpN210(object):

    """Implementation of UsrpN210 driver"""

    def __init__(self, addr, samp_freq=5e6, center_freq=2.412e9, sample_format='fc32'):
        self.uhd = uhd.usrp_source("addr=" + addr,
                                   uhd.stream_args(
                                       cpu_format=sample_format,
                                       channels=range(1),
                                   ))
        self.samp_freq = samp_freq
        self.uhd.set_samp_rate(self.samp_freq)
        self.uhd.set_gain(10, 0)
        self.uhd.set_antenna("TX/RX", 0)
        self.uhd.set_bandwidth(self.samp_freq / 2, 0)
        lo_offset = 12e6
        self.uhd.set_center_freq(uhd.tune_request(center_freq, lo_offset), 0)
        self.window = [0]

    def generate(self, num_samples):
        if len(self.window) != num_samples:
            self.window = signal.blackmanharris(num_samples)

        orig_signal = self.uhd.finite_acquisition(num_samples * 100)
        return orig_signal[:num_samples] * self.window

    def parse_options(self, options):
        for key, opt in options.items():
            if key == 'antenna_gain':
                self.uhd.set_gain(opt, 0)
            if key == 'center_freq':
                self.uhd.set_center_freq(opt * 1e6, 0)
