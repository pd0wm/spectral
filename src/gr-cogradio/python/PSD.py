import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt
import scipy.fftpack as fftp


class PSD(gr.sync_block):

    """
    PSD
    """

    def __init__(self, length):
        self.length = length
        gr.sync_block.__init__(self,
                               name="PSD",
                               in_sig=[(np.float32, 2 * self.length - 1)],
                               out_sig=None)

        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.fig.show()

    def work(self, input_items, output_items):
        in0 = input_items[0]
        self.axes.clear()
        Y = fftp.fft(in0[0])
        Y = np.abs(Y[0:len(Y)/2])
        self.axes.plot(Y)
        self.axes.set_title("PSD")
        plt.draw()
        return len(input_items[0])
