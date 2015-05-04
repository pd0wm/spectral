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
                               in_sig=[np.float32],
                               out_sig=[(np.float32, 2 * self.length - 1)])
        self.buffer = np.zeros(self.length)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for i in range(len(in0)):
            out[i] = self.workItem(in0[i])
        return len(output_items[0])

    def workItem(self, item):
        self.buffer = np.delete(np.append(self.buffer, item), 1)

        if self.count % self.frequency == 0:
            self.rx = np.correlate(
                self.buffer, self.buffer, 'full') / float(self.length)
        self.count += 1

        return self.rx
