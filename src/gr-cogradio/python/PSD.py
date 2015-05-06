import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt
import scipy.fftpack as fftp


class PSD(gr.sync_block):

    """
    PSD
    """

    count = 1

    def __init__(self, length, frequency):
        self.length = length
        self.frequency = frequency
        gr.sync_block.__init__(self,
                               name="PSD",
                               in_sig=[(np.complex64, self.length)],
                               out_sig=None)

        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.fig.show()

    def work(self, input_items, output_items):
        in0 = input_items[0]

        self.count += 1
        if self.count == self.frequency:
            self.axes.clear()
            Y = fftp.fftshift(fftp.fft(in0[0]))
            Y = np.log10(np.abs(Y)) * 20
            self.axes.plot(Y)
            self.axes.set_title("PSD")
            self.axes.set_ylim([-140, -20])
            plt.draw()
            self.count = 0

        return len(input_items[0])
