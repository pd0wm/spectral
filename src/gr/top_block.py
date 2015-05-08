#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri May  8 16:16:40 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cogradio
import time
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.length = length = 500
        self.gain = gain = 50
        self.center = center = 1.396e9
        self.N = N = 14

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=1000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        _center_sizer = wx.BoxSizer(wx.VERTICAL)
        self._center_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	label='center',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._center_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_center_sizer,
        	value=self.center,
        	callback=self.set_center,
        	minimum=500e6,
        	maximum=2.5e9,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_center_sizer)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(center, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.cogradio_vector_plot_0_2 = cogradio.vector_plot(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=966,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.cogradio_vector_plot_0_2.win)
        self.cogradio_vector_plot_0_0 = cogradio.vector_plot(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=500,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.cogradio_vector_plot_0_0.win)
        self.cogradio_vector_fft_0_0 = cogradio.vector_fft(500)
        self.cogradio_vector_fft_0 = cogradio.vector_fft(966)
        self.cogradio_mc_sampling_0 = cogradio.mc_sampling(length, N)
        self.cogradio_mc_crosscorr_0 = cogradio.mc_crosscorr(length, N)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, length)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((966 * [gain]))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.cogradio_vector_plot_0_2, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.cogradio_mc_sampling_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.cogradio_vector_fft_0_0, 0))    
        self.connect((self.cogradio_mc_crosscorr_0, 0), (self.cogradio_vector_fft_0, 0))    
        self.connect((self.cogradio_mc_sampling_0, 0), (self.cogradio_mc_crosscorr_0, 0))    
        self.connect((self.cogradio_vector_fft_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.cogradio_vector_fft_0_0, 0), (self.cogradio_vector_plot_0_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.cogradio_vector_plot_0_0.set_sample_rate(self.samp_rate)
        self.cogradio_vector_plot_0_2.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.blocks_multiply_const_vxx_0.set_k((966 * [self.gain]))

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        self._center_slider.set_value(self.center)
        self._center_text_box.set_value(self.center)
        self.uhd_usrp_source_0.set_center_freq(self.center, 0)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
