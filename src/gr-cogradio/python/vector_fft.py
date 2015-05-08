#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr
import scipy.fftpack as fftp

class vector_fft(gr.sync_block):
    """
    docstring for block vector_fft
    """
    def __init__(self, vector_length=100):
        self.tmr = 0
        self.vector_length = vector_length
        
        gr.sync_block.__init__(self,
            name="vector_fft",
            in_sig=[(np.complex64, self.vector_length)],
            out_sig=[(np.complex64, self.vector_length)])


    def work(self, input_items, output_items):
        in_0 = input_items[0]
        out_0 = output_items[0]

        for i, input_ndarray in enumerate(in_0):
            #out_0[i] = 20 * np.log10(np.abs(fftp.fftshift(fftp.fft(input_ndarray))))
            out_0[i] = 1000 * np.abs(fftp.fftshift(fftp.fft(input_ndarray)))
            self.tmr = 0

        return len(output_items[0])

