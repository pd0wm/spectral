#!/usr/bin/env python
import cogradio as cg
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
parser.add_argument('-source', metavar='source', type=str, default='dump')
parser.add_argument('-snr', metavar='snr', type=str, default=None)
parser.add_argument('-dump', metavar='file', type=str, default='twotone.dmp')
args = parser.parse_args()

ip = args.ip
L = args.L
N = args.N
sample_freq = args.f_samp
dump_file_path = args.dump
source_type = args.source.lower()
source_snr = args.snr

frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 2.41e9
multiplier = 100  # Warning: greatly diminishes perfomance
nyq_block_size = L * N * multiplier
window_length = nyq_block_size
threshold = 2000

if source_type == "usrp":
    source = cg.source.UsrpN210(addr=ip, samp_freq=sample_freq, center_freq=center_freq)
elif source_type == "dump":
    source = cg.source.File(dump_file_path)
elif source_type == "complex":
    source = cg.source.ComplexExponential(frequencies, sample_freq, SNR=source_snr)

sampler = cg.sampling.MultiCoset(N)
reconstructor = cg.reconstruction.Wessel(N, L)

# Init processes
signal_queue = Queue(10)
websocket_src_queue = Queue(10)
websocket_rec_queue = Queue(10)
websocket_det_queue = Queue(10)

parent_opt_src, child_opt_src = Pipe()
parent_opt_rec, child_opt_rec = Pipe()
parent_opt_web, child_opt_web = Pipe()

if __name__ == '__main__':

    p1 = Process(target=run_generator,
                 args=(signal_queue, websocket_src_queue, source, sampler, sample_freq, window_length, child_opt_src))
    p2 = Process(target=run_reconstructor,
                 args=(signal_queue, websocket_rec_queue, reconstructor, sample_freq, center_freq, child_opt_rec))
    p3 = Process(target=run_websocket_server,
                 args=(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq, center_freq, child_opt_web))
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
