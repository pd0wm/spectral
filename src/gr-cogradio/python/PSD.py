import numpy as np
from gnuradio import gr
import matplotlib.pyplot as plt
import scipy.fftpack as fftp


class PSD(gr.sync_block):

    """
    PSD
    """

    count = 1

    def __init__(self, samp_rate, length, frequency):
        self.samp_rate = samp_rate
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
            ylim_prev = self.axes.get_ylim()
            self.axes.clear()
            Y = np.abs(fftp.fftshift(fftp.fft(in0[0])))
            # Y = np.log10(np.abs(Y)) * 20
            self.axes.plot(Y)

            ylim_new = self.axes.get_ylim()
            self.set_xaxis()
            self.set_yaxis(ylim_prev, ylim_new)

            self.axes.set_title("PSD")
            plt.draw()
            self.count = 0

        return len(input_items[0])

    def set_xaxis(self):
        xmax = self.samp_rate / 2
        labels = np.arange(0, xmax / 1000, 5)
        labels = np.concatenate((-labels[1::][::-1], labels))
        ticks = labels * self.length / self.samp_rate * 1000 + self.length / 2

        self.axes.set_xlim((0, self.length))
        self.axes.set_xticks(ticks)
        self.axes.set_xticklabels(labels)

    def set_yaxis(self, ylim_prev, ylim_new):
        if ylim_prev[0] < ylim_new[0]:
            self.axes.set_ylim(ymin=ylim_prev[0])

        if ylim_prev[1] > ylim_new[1]:
            self.axes.set_ylim(ymax=ylim_prev[1])
