#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Jun  7 16:53:40 2015
##################################################
import Pyro4


queue = Pyro4.Proxy("PYRONAME:jamqueue")

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import threading
import time
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.jammer_gain = jammer_gain = 0
        self.jammer_center = jammer_center = 0

        ##################################################
        # Blocks
        ##################################################

        def _jammer_center_probe():
            while True:
                val = self.get_jammer_center()
                try:
                    self.set_jammer_center(val)
                except AttributeError:
                    pass
                time.sleep(1.0)
        _jammer_center_thread = threading.Thread(target=_jammer_center_probe)
        _jammer_center_thread.daemon = True
        _jammer_center_thread.start()
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate/64)
        self.uhd_usrp_sink_0.set_center_freq(jammer_center, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(jammer_gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(samp_rate/2, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_UNIFORM, 1, 0, 8192)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.uhd_usrp_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 12.5e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate/64)
        self.uhd_usrp_sink_0.set_bandwidth(self.samp_rate/2, 0)

    def get_jammer_gain(self):
        return self.jammer_gain

    def set_jammer_gain(self, jammer_gain):
        if hasattr(self, 'uhd_usrp_sink_0'):
            self.jammer_gain = jammer_gain
            self.uhd_usrp_sink_0.set_gain(self.jammer_gain, 0)

    def get_jammer_center(self):
        self.set_jammer_gain(-100)
        self.set_jammer_center(2.4e9)
        print "UIT"
        time.sleep(0.2)

        rd = queue.read()
        if rd:
            self.set_jammer_gain(30)
            print "AAN"
            print rd
            return 446e6
            return rd
        else:
            self.set_jammer_gain(-100)
            return 2.4e9


    def set_jammer_center(self, jammer_center):
        if hasattr(self, 'uhd_usrp_sink_0'):
            self.jammer_center = jammer_center
            self.uhd_usrp_sink_0.set_center_freq(self.jammer_center, 0)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
