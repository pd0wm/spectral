#!/usr/bin/env python
import cogradio as cg
import cogradio_vis as vis
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
a = 5
b = 3
N = a * b
upscale_factor = 50  # Warning: greatly diminishes performance
block_size = N * upscale_factor * L

settings = Pyro4.Proxy("PYRONAME:cg.settings")
settings.update({
    'Pfa': 0.1,
    'center_freq': 2.4,  # GHz
    'num_bins': 150,
    'window_length': 50,
    'antenna_gain': 10
})

if source_type == "usrp":
    source = cg.source.UsrpN210(addr=ip, samp_freq=sample_freq)
elif source_type == "dump":
    source = cg.source.File(dump_file_path)
elif source_type == "complex":
    source = cg.source.ComplexExponential(frequencies, sample_freq, SNR=source_snr)


# sampler = cg.sampling.Coprime(a, b)
sampler = cg.sampling.MultiCoset(N)


reconstructor = cg.reconstruction.Wessel(L, sampler.get_C())
# reconstructor = cg.reconstruction.CrossCorrelation(N, L, C=sampler.get_C())
detector = cg.detection.noise_power()

# Init processes
signal_queue = vis.multiprocessing.SafeQueue()
detection_queue = vis.multiprocessing.SafeQueue()

websocket_src_queue = vis.multiprocessing.SafeQueue()
websocket_rec_queue = vis.multiprocessing.SafeQueue()
websocket_det_queue = vis.multiprocessing.SafeQueue()


if __name__ == '__main__':

    p1 = Process(target=run_generator,
                 args=(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor))
    p2 = Process(target=run_reconstructor,
                 args=(signal_queue, websocket_rec_queue, detection_queue, reconstructor, sample_freq))
    p3 = Process(target=run_websocket_server,
                 args=(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq))
    p4 = Process(target=run_detector,
                 args=(detector, detection_queue, websocket_det_queue))
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
