#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon May  4 14:38:03 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
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
        self.samp_rate = samp_rate = 100e3
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
        self.cogradio_autocorrelation_0 = cogradio.autocorrelation(100, 50)
        self.cogradio_PSD_0 = cogradio.PSD(100)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, cos_freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, samp_rate/10, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.cogradio_autocorrelation_0, 0), (self.cogradio_PSD_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.cogradio_autocorrelation_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_cos_freq(self.samp_rate/4)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_frequency(self.samp_rate/10)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_cos_freq(self):
        return self.cos_freq

    def set_cos_freq(self, cos_freq):
        self.cos_freq = cos_freq
        self._cos_freq_slider.set_value(self.cos_freq)
        self._cos_freq_text_box.set_value(self.cos_freq)
        self.analog_sig_source_x_1.set_frequency(self.cos_freq)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
