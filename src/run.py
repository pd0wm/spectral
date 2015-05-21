#!/usr/bin/env python
import cogradio_utils as cg
import argparse
import time
from processes import *
from multiprocessing import Process, Queue, Pipe


# Set up initial parameters
parser = argparse.ArgumentParser(description='Cognitive radio compressive sensing process')
parser.add_argument('-ip', metavar='ip', type=str, default='192.168.10.2')
parser.add_argument('-f_samp', metavar='f_samp', type=int, default=10e6)
parser.add_argument('-N', metavar='N', type=int, default=14)
parser.add_argument('-L', metavar='L', type=int, default=40)
args = parser.parse_args()

ip = args.ip
L = args.L
N = args.N
sample_freq = args.f_samp

frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 2.41e9
multiplier = 100  # Warning: greatly diminishes perfomance
nyq_block_size = L * N * multiplier
window_length = nyq_block_size
threshold = 2000

# Init blocks
try:
    source = cg.source.UsrpN210(addr=ip, samp_freq=sample_freq, center_freq=center_freq)
except RuntimeError:
    print "Could not find USRP, falling back to artificial source"
    source = cg.source.ComplexExponential(frequencies, f_samp, SNR=5)

sampler = cg.sampling.MultiCoset(N)
reconstructor = cg.reconstruction.Wessel(N, L)

# Init processes
signal_queue = Queue(10)
websocket_queue = Queue(10)

parent_opt_src, child_opt_src = Pipe()
parent_opt_rec, child_opt_rec = Pipe()
parent_opt_web, child_opt_web = Pipe()

if __name__ == '__main__':

    p1 = Process(target=run_generator,
                 args=(signal_queue, source, sampler, sample_freq, window_length, child_opt_src))
    p2 = Process(target=run_reconstructor,
                 args=(signal_queue, websocket_queue, reconstructor, sample_freq, center_freq, child_opt_rec))
    p3 = Process(target=run_websocket_server,
                 args=(websocket_queue, sample_freq, center_freq, child_opt_web))
    p4 = Process(target=run_settings_server,
                 args=(parent_opt_web, parent_opt_src, parent_opt_rec))
    processes = [p1, p2, p3, p4]

    try:
        [p.start() for p in processes]
        [p.join() for p in processes]
    except KeyboardInterrupt:
        flag = True
        while flag:
            flag = False
            for p in processes:
                if p.is_alive():
                    flag = True
                    p.terminate()
                    print p, "termination sent"
            time.sleep(1)
    finally:
        sys.exit(1)
