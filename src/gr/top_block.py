#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed May  6 17:58:09 2015
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import cogradio
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32e3
        self.length = length = 700
        self.cos_freq = cos_freq = samp_rate/4

        ##################################################
        # Blocks
        ##################################################
        _cos_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._cos_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_cos_freq_sizer,
        	value=self.cos_freq,
        	callback=self.set_cos_freq,
        	label='cos_freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._cos_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_cos_freq_sizer,
        	value=self.cos_freq,
        	callback=self.set_cos_freq,
        	minimum=0,
        	maximum=samp_rate/2,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_cos_freq_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.cogradio_mc_sampling_0 = cogradio.mc_sampling(length, 6, 14)
        self.cogradio_mc_crosscorr_0 = cogradio.mc_crosscorr(length, 6, 14)
        self.cogradio_PSD_0 = cogradio.PSD(1386, 10)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, length)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, cos_freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2e3, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.cogradio_mc_sampling_0, 0))    
        self.connect((self.cogradio_mc_crosscorr_0, 0), (self.cogradio_PSD_0, 0))    
        self.connect((self.cogradio_mc_sampling_0, 0), (self.cogradio_mc_crosscorr_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_cos_freq(self.samp_rate/4)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def get_cos_freq(self):
        return self.cos_freq

    def set_cos_freq(self, cos_freq):
        self.cos_freq = cos_freq
        self._cos_freq_slider.set_value(self.cos_freq)
        self._cos_freq_text_box.set_value(self.cos_freq)
        self.analog_sig_source_x_1.set_frequency(self.cos_freq)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
