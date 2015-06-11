import numpy as np
import Pyro4


class Jammer(object):

    def __init__(self, sample_freq, center_freq):
        self.sample_freq = sample_freq
        self.center_freq = center_freq
        self.queue = Pyro4.Proxy("PYRONAME:jamqueue")

    def parse_options(self, options):
        for key, value in options.items():
            if key == "center_freq":
                self.center_freq = value * 1e9
            elif key == "sample_freq":
                self.sample_freq = value

    def find_longest_consecutive(self, det):
        det2 = det + [0]
        max_length = 0
        max_start = 0
        max_stop = 0
        cur_length = 0
        cur_start = 0
        cur_one = False
        for i, d in enumerate(det2):
            if d == 0:
                if cur_length > max_length:
                    max_length = cur_length
                    max_start = cur_start
                    max_stop = i - 1
                    cur_one = False
            else:
                if not cur_one:
                    cur_start = i
                    cur_length = 0
                    cur_one = True

                cur_length += 1

        return (max_start, max_stop)

    def jam(self, det):
        start = self.center_freq - 0.5*self.sample_freq
        stop = self.center_freq + 0.5*self.sample_freq

        freqs = np.linspace(start, stop, len(det))

        max_start, max_stop = self.find_longest_consecutive(det)
        if max_stop - max_start > 5:
            jam_freq = (freqs[max_start] + freqs[max_stop]) / 2.0
            self.queue.send(jam_freq)
            print jam_freq
        else:
            self.queue.send(None)
            print
