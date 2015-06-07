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
parser.add_argument('-L', metavar='L', type=int, default=40)
parser.add_argument('-source', metavar='source', type=str, default='complex')
parser.add_argument('-snr', metavar='snr', type=str, default=None)
parser.add_argument('-dump', metavar='file', type=str, default='dumps/twotone.dmp')
args = parser.parse_args()

ip = args.ip
L = args.L
sample_freq = args.f_samp
dump_file_path = args.dump
source_type = args.source.lower()
source_snr = args.snr

frequencies = [2e6, 4e6, 4.5e6, 3e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 466e6
a = 5
b = 3
N = a * b
upscale_factor = 50  # Warning: greatly diminishes performance
block_size = N * upscale_factor * L

threshold = 2000
num_bins = 20
window_length = 50
Pfa = 0.1  # Doet niks sur le moment

if source_type == "usrp":
    source = cg.source.UsrpN210(addr=ip, samp_freq=sample_freq, center_freq=center_freq)
elif source_type == "dump":
    source = cg.source.File(dump_file_path)
elif source_type == "complex":
    source = cg.source.ComplexExponential(frequencies, sample_freq, SNR=source_snr)


# sampler = cg.sampling.Coprime(a, b)
sampler = cg.sampling.MultiCoset(N)


reconstructor = cg.reconstruction.Wessel(L, sampler.get_C())
# reconstructor = cg.reconstruction.CrossCorrelation(N, L, C=sampler.get_C())
detector = cg.detection.noise_power(threshold, Pfa, window_length, num_bins)

# Init processes
signal_queue = Queue(2)
detection_queue = Queue(2)
websocket_src_queue = Queue(10)
websocket_rec_queue = Queue(10)
websocket_det_queue = Queue(10)

opt_src = Queue(10)
opt_rec = Queue(10)
opt_web = Queue(10)
opt_det = Queue(10)

if __name__ == '__main__':

    p1 = Process(target=run_generator,
                 args=(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor, opt_src))
    p2 = Process(target=run_reconstructor,
                 args=(signal_queue, websocket_rec_queue, detection_queue, reconstructor, sample_freq, center_freq, opt_rec))
    p3 = Process(target=run_websocket_server,
                 args=(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq, center_freq, opt_web))
    p4 = Process(target=run_settings_server,
                 args=(opt_web, opt_src, opt_rec, opt_det))
    p5 = Process(target=run_detector,
                 args=(detector, detection_queue, websocket_det_queue, sample_freq, center_freq, opt_det))
    p6 = Process(target=run_jam_queue)

    processes = [p1, p2, p3, p4, p5, p6]

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
