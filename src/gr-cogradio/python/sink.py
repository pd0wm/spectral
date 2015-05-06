import numpy
from gnuradio import gr
import time


class sink(gr.sync_block):

    """
    just a brain dead block
    """

    countFrequency = 0
    frequency = 10000
    countStay = 0
    stay = 10000/frequency
    timeMs = 0

    def __init__(self):
        gr.sync_block.__init__(self,
                               name="sink",
                               in_sig=[numpy.complex64],
                               out_sig=None)

    def work(self, input_items, output_items):
        in0 = input_items[0]

        self.countFrequency += 1
        if self.countFrequency == self.frequency:
            self.countStay += 1
            if self.countStay == self.stay:
                self.timeMs += 0.1
                print "Delay (ms): " + str(self.timeMs) + ", block size: " + str(len(in0)) + ", frequency: " + str(self.frequency)
                self.countStay = 0
            time.sleep(self.timeMs / 1000)
            self.countFrequency = 0

        return len(input_items[0])
