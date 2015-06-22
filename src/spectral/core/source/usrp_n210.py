from .source import Source
import numpy as np
try:
    from gnuradio import uhd
except ImportError:
    class uhd:
        def usrp_source(*args, **kwargs):
            raise RuntimeError("UHD lib not installed")


class UsrpN210(Source):

    """
    Signal coming from a USRP N210 radio. This class starts a connection
    with the radio and provides methods for receiving samples,
    setting center frequency and gain values. The local oscillator offset
    is needed because the automatic dc offset calibration does not work
    with the finite_acquisition function.


    Args:
        addr: IP address of the USRP
        samp_freq: Sample frequency of the USRP
        center_freq: Initial center frequency on initialisation
        lo_ffset: Local oscillator offset
        gain: Amount of antenna gain (dB)
        sample_format: Output datatype of the USRP
    """

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
        """
        Method to tune the USRP to the desired frequency.

        Args:
            frequency: Desired center freqeuncy
        """
        if self.center_freq != frequency:
            print "Tuning to", frequency / 1e9, "GHz"
            self.center_freq = frequency
            self.uhd.set_center_freq(uhd.tune_request(frequency, self.lo_offset), 0)

    def set_gain(self, gain):
        """
        Method to set the antenna gain on the USRP

        Args:
            gain: Desired gain in dB
        """
        if self.gain != gain:
            self.gain = gain
            self.uhd.set_gain(gain, 0)

    def generate(self, num_samples):
        """
        Method to get samples from the USRP. The first few samples are
        thrown away due to unwanted spikes.

        Args:
            num_samples: Desired number of samples

        Returns:
            Samples from the USRP

        """
        samples = self.uhd.finite_acquisition(num_samples + 1000)[1000:]
        samples -= np.mean(samples)

        if len(samples) != num_samples:
            raise RuntimeError("Number of samples from USRP incorrect")

        return np.array(samples)

    def parse_options(self, options):
        """
        Method to parse options from the client. Calls the necessary
        helper functions to change settings.

        Possible keys: 'antenna_gain' and 'center_freq'

        Args:
            options: Dictionary with options

        """
        for key, value in options.items():
            if key == 'antenna_gain':
                self.set_gain(value)
            if key == 'center_freq':
                self.set_frequency(value * 1e9)
