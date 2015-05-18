from gnuradio import uhd


class UsrpN210(object):

    """Implementation of UsrpN210 driver"""

    def __init__(self, addr, center_freq=2.412e9, sample_format='fc32'):
        self.uhd = uhd.usrp_source("addr=" + addr,
                                   uhd.stream_args(
                                       cpu_format=sample_format,
                                       channels=range(1),
                                   ))
        self.samp_freq = 20e6
        self.uhd.set_samp_rate(self.samp_freq)
        self.uhd.set_gain(10, 0)
        self.uhd.set_antenna("TX/RX", 0)
        self.uhd.set_bandwidth(self.samp_freq / 2, 0)
        self.uhd.set_center_freq(center_freq, 0)

    def generate(self, samp_freq, num_samples):
        if samp_freq != self.samp_freq:
            self.samp_freq = samp_freq

            self.uhd.set_samp_rate(samp_freq)
            self.uhd.set_bandwidth(samp_freq / 2, 0)

        return self.uhd.finite_acquisition(num_samples)
