#!/usr/bin/env python

import numpy as np
from gnuradio import gr
import cogradio_utils as cg


class mc_sampling(gr.sync_block):

    """
    docstring for block mc_sampling
    """

    def __init__(self, chunk_size, m, n):
        self.chunk_size = chunk_size
        self.m = m
        self.n = n
        self.sampler = cg.sampling.MultiCoset(14)
        gr.sync_block.__init__(self,
                               name="mc_sampling",
                               in_sig=[(np.complex64, self.chunk_size)],
                               out_sig=[(np.complex64, (self.m, int(self.chunk_size / self.n)))])

    def work(self, input_items, output_items):
        in_0 = input_items[0]
        out_0 = output_items[0]

        for i, input_vector in enumerate(in_0):
            out_0[i] = self.sampler.sample(np.real(input_vector))

        return len(output_items[0])
