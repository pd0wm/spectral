import numpy as np
from gnuradio import gr


class autocorrelation(gr.sync_block):

    """
    docstring for block autocorrelation
    """

    count = 0

    def __init__(self, length, frequency):
        self.length = length
        self.frequency = frequency
        gr.sync_block.__init__(self,
                               name="autocorrelation",
                               in_sig=[np.complex64],
                               out_sig=[(np.complex64, 2 * self.length - 1)])
        self.buffer = np.zeros(self.length)
        self.rx = np.zeros(2 * self.length - 1)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        self.count += 1
        if self.count == self.frequency:
            if len(in0) - self.length >= 0:
                sig = in0[(len(in0) - self.length):len(in0)]
            else:
                sig = np.append(np.zeros(self.length - len(in0)), in0)

            self.rx = np.correlate(
                sig, sig, 'full') / float(self.length)
            self.count = 0

        out[:] = np.tile(self.rx, (len(out), 1))
        return len(out)
