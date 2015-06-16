#!/usr/bin/env python
import cogradio as cg
import cogradio_vis as vis
import argparse
import time
import sys
from processes import *
from multiprocessing import Process, Queue, Pipe


# Set up initial parameters
parser = argparse.ArgumentParser(description='Cognitive radio compressive sensing process')
parser.add_argument('-ip', metavar='ip', type=str, default='192.168.10.2')
parser.add_argument('-f_samp', metavar='f_samp', type=int, default=10e6)
parser.add_argument('-L', metavar='L', type=int, default=40)
parser.add_argument('-source', metavar='source', type=str, default='dump')
parser.add_argument('-snr', metavar='snr', type=str, default=None)
parser.add_argument('-dump', metavar='file', type=str, default='dumps/ofdm.dmp')
args = parser.parse_args()

ip = args.ip
L = args.L
sample_freq = args.f_samp
dump_file_path = args.dump
source_type = args.source.lower()
source_snr = args.snr

frequencies = [2e6, 4e6, 4.5e6, 3e6]
widths = [1000, 1000, 1000, 1000]
L = 3
a = 5
b = 7
N = 61
upscale_factor = 2000  # Warning: greatly diminishes performance
block_size = N * upscale_factor * L

settings = Pyro4.Proxy("PYRONAME:cg.settings")
settings.update({
    'source': source_type,
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
elif source_type == "sinusoidal":
    source = cg.source.Sinusoidal(frequencies, sample_freq, SNR=source_snr)


sampler = cg.sampling.Coprime(a, b)
# sampler = cg.sampling.MultiCoset(N)


reconstructor = cg.reconstruction.Wessel(L, sampler.get_C())
# reconstructor = cg.reconstruction.CrossCorrelation(N, L, C=sampler.get_C())
detector = cg.detection.noise_power()

# Init queues
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
    p3 = Process(target=run_detector,
                 args=(detector, detection_queue, websocket_det_queue))
    p4 = Process(target=run_server,
                 args=())
    p5 = Process(target=run_websocket_control,
                 args=())
    p6 = Process(target=run_websocket_data,
                 args=(websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq))
    p7 = Process(target=run_jam_queue,
                 args=())

    processes = [p1, p2, p3, p4, p5, p6, p7]

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
