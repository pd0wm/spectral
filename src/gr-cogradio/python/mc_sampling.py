#!/usr/bin/env python

import numpy as np
from gnuradio import gr
import cogradio_utils as cg


class mc_sampling(gr.sync_block):

    """
    docstring for block mc_sampling
    """

    def __init__(self, chunk_size, m):
        self.chunk_size = chunk_size
        self.m = m
        self.sampler = cg.sampling.MultiCoset(14)
        gr.sync_block.__init__(self,
                               name="mc_sampling",
                               in_sig=[(np.complex64, self.chunk_size)],
                               out_sig=[(np.complex64, (self.chunk_size, self.m))])

    def work(self, input_items, output_items):
        in_0 = input_items[0]
        out_0 = output_items[0]

        for i, input_vector in enumerate(in_0):
            # print np.tile((input_vector), self.m).reshape((self.chunk_size, self.m)).shape
            print np.real(input_vector)
            print self.sampler.sample(np.real(input_vector))
            out_0[i] = np.zeros((self.chunk_size, self.m))

        return len(output_items[0])
