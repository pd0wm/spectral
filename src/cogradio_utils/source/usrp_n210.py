from gnuradio import uhd


class UsrpN210(object):

    """Implementation of UsrpN210 driver"""

    def __init__(self, addr, center_freq=2.412e9, sample_format='fc32'):
        self.uhd = uhd.usrp_source("addr=" + addr,
                                   uhd.stream_args(
                                       cpu_format=sample_format,
                                       channels=range(1),
                                   ))
        self.uhd.set_antenna("TX/RX")
        self.uhd.set_center_freq(center_freq)
        self.samp_freq = None

    def generate(self, samp_freq, duration):
        num_samples = samp_freq * duration

        if samp_freq != self.samp_freq:
            self.samp_freq = samp_freq

            self.uhd.set_samp_rate(samp_freq)
            self.uhd.set_bandwidth(samp_freq / 2)

        return self.uhd.finite_acquisition(num_samples)
