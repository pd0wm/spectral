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
import cogradio_utils as cg

class SPFL(gr.sync_block):
    """
    docstring for block SPFL
    """
    def __init__(self, length):
        self.length = length
        self.detector = cg.detection.SPFL()
        gr.sync_block.__init__(self,
            name="SPFL",
            in_sig=[(np.complex64, self.length)],
            out_sig=[(np.complex64, 1)])


    def work(self, input_items, output_items):
        # select first vector for rx
        in0 = input_items[0][0]
        self.detector.detect(in0)
        out = output_items[0]
        print(output_items[0].shape)
        return len(output_items[0])

