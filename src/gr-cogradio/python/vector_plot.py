#!/usr/bin/env python
from __future__ import division


import fft_window
import common
from gnuradio import gr, fft
from gnuradio import analog
from gnuradio import blocks
from gnuradio.fft import logpwrfft
from pubsub import pubsub
from constants import *
import math

class vector_plot(gr.hier_block2, common.wxgui_hb):
	"""
	An fft block with real/complex inputs and a gui window.
	"""

	def __init__(
		self,
		parent,
		baseband_freq=0,
		ref_scale=1.0,
		y_per_div=10,
		y_divs=8,
		ref_level=1,
		sample_rate=1,
		fft_size=100,
		fft_rate=fft_window.DEFAULT_FRAME_RATE,
		average=False,
		avg_alpha=None,
		title='',
		size=fft_window.DEFAULT_WIN_SIZE,
		peak_hold=False,
		win=None,
                use_persistence=False,
                persist_alpha=None,
		**kwargs #do not end with a comma
	):
		#ensure avg alpha
		if avg_alpha is None: avg_alpha = 2.0/fft_rate
                #ensure analog alpha
                if persist_alpha is None:
                  actual_fft_rate=float(sample_rate/fft_size)/float(max(1,int(float((sample_rate/fft_size)/fft_rate))))
                  #print "requested_fft_rate ",fft_rate
                  #print "actual_fft_rate    ",actual_fft_rate
                  analog_cutoff_freq=0.5 # Hertz
                  #calculate alpha from wanted cutoff freq
                  persist_alpha = 1.0 - math.exp(-2.0*math.pi*analog_cutoff_freq/actual_fft_rate)

		#init
		gr.hier_block2.__init__(
			self,
			"cogradio_sink",
			gr.io_signature(1, 1, gr.sizeof_gr_complex * fft_size),
			gr.io_signature(0, 0, 0),
		)

		msgq = gr.msg_queue(2)
		sink = blocks.message_sink(gr.sizeof_gr_complex * fft_size, msgq, True)

                def get_sample_rate(tmp=None):
                        return sample_rate

                def iets(tmp=None):
                        return 1.0

                #controller
		self.controller = pubsub()
                self.controller.subscribe(AVERAGE_KEY, iets)
		self.controller.publish(AVERAGE_KEY, iets)
		self.controller.subscribe(AVG_ALPHA_KEY, iets)
		self.controller.publish(AVG_ALPHA_KEY, iets)
		self.controller.subscribe(SAMPLE_RATE_KEY, iets)
		self.controller.publish(SAMPLE_RATE_KEY, get_sample_rate)
                
		#start input watcher
		common.input_watcher(msgq, self.controller, MSG_KEY)
		#create window
		self.win = fft_window.fft_window(
			parent=parent,
			controller=self.controller,
			size=size,
			title=title,
			real=False,
			fft_size=fft_size,
			baseband_freq=baseband_freq,
			sample_rate_key=SAMPLE_RATE_KEY,
			y_per_div=y_per_div,
			y_divs=y_divs,
			ref_level=ref_level,
			average_key=AVERAGE_KEY,
			avg_alpha_key=AVG_ALPHA_KEY,
			peak_hold=peak_hold,
			msg_key=MSG_KEY,
                        use_persistence=use_persistence,
                        persist_alpha=persist_alpha,
		)
		common.register_access_methods(self, self.win)
		setattr(self.win, 'set_baseband_freq', getattr(self, 'set_baseband_freq')) #BACKWARDS
		setattr(self.win, 'set_peak_hold', getattr(self, 'set_peak_hold')) #BACKWARDS
		#connect
		self.wxgui_connect(self, sink)

	def set_callback(self,callb):
		self.win.set_callback(callb)