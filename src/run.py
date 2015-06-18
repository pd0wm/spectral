#!/usr/bin/env python
import cogradio as cg
import cogradio_vis as vis
import argparse
import time
import sys
import processes as pr
from multiprocessing import Process


# Set up initial parameters
parser = argparse.ArgumentParser(description='Cognitive radio compressive sensing process')
parser.add_argument('-ip', metavar='ip', type=str, default='192.168.10.2')
parser.add_argument('-f_samp', metavar='f_samp', type=int, default=10e6)
parser.add_argument('-L', metavar='L', type=int, default=40)
parser.add_argument('-source', metavar='source', type=str, default='sinusoidal')
parser.add_argument('-snr', metavar='snr', type=float, default=None)
parser.add_argument('-dump', metavar='file', type=str, default='dumps/ofdm.dmp')
parser.add_argument('-controlport', metavar='controlport', type=int, default=1338)
parser.add_argument('-dataport', metavar='dataport', type=int, default=1337)
args = parser.parse_args()

ip = args.ip
L = args.L
sample_freq = args.f_samp
dump_file_path = args.dump
source_type = args.source.lower()
source_snr = args.snr
control_port = args.controlport
data_port = args.dataport

frequencies = [2e6, 4e6, 4.5e6, 3e6]
widths = [1000, 1000, 1000, 1000]
L = 3
a = 5
b = 7
N = 61
upscale_factor = 2000  # Warning: greatly diminishes performance
block_size = N * upscale_factor * L

settings = vis.get_settings_object()
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
elif source_type == "sinusoidal":
    source = cg.source.Sinusoidal(frequencies, sample_freq, SNR=source_snr)


# sampler = cg.sampling.Coprime(a, b)
sampler = cg.sampling.MultiCoset(N)

reconstructor = cg.reconstruction.Wessel(L, sampler.get_C(), cache=False)
# reconstructor = cg.reconstruction.CrossCorrelation(L, C=sampler.get_C())

detector = cg.detection.noise_power()

# Init queues
signal_queue = vis.multiprocessing.SafeQueue()
detection_queue = vis.multiprocessing.SafeQueue()

websocket_src_queue = vis.multiprocessing.SafeQueue()
websocket_rec_queue = vis.multiprocessing.SafeQueue()
websocket_det_queue = vis.multiprocessing.SafeQueue()


if __name__ == '__main__':

    p1 = Process(target=pr.run_generator,
                 args=(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor))
    p2 = Process(target=pr.run_reconstructor,
                 args=(signal_queue, websocket_rec_queue, detection_queue, reconstructor, sample_freq))
    p3 = Process(target=pr.run_detector,
                 args=(detector, detection_queue, websocket_det_queue))
    p4 = Process(target=pr.run_server,
                 args=())
    p5 = Process(target=pr.run_websocket_control,
                 args=(control_port,))
    p6 = Process(target=pr.run_websocket_data,
                 args=(data_port, websocket_src_queue, websocket_rec_queue, websocket_det_queue, sample_freq))

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
