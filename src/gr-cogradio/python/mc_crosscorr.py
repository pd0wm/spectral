#!/usr/bin/env python

import numpy as np
from gnuradio import gr

class mc_crosscorr(gr.sync_block):
    """
    docstring for block mc_crosscorr
    """
    def __init__(self, chunk_size, m, n):
        self.m = m
        self.n = n
        self.l = chunk_size / n
        gr.sync_block.__init__(self,
                               name="mc_crosscorr",
                               in_sig=[(np.complex64, (self.m, self.l))],
                               out_sig=[(np.complex64, self.n * (2 * self.l - 1))])


    def work(self, input_items, output_items):
        in_0 = input_items[0]
        out_0 = output_items[0]

        for i, input_ndarray in enumerate(in_0):
            out_0[i] = [0] * self.n * (2 * self.l - 1)

        return len(output_items[0])

