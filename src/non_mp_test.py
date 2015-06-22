import spectral.core as sc
import spectral.supervisor as ss
from multiprocessing import Process
import processes as pr
import time

dump_file_path = 'dumps/ofdm.dmp'
L = 3
a = 3
b = 4
N = 51
upscale_factor = 2000  # Warning: greatly diminishes performance
sample_freq = 10e6
block_size = N * upscale_factor * L
source = sc.source.File(dump_file_path)
sampler = sc.sampling.MinimalSparseRuler(N)
reconstructor = sc.reconstruction.Wessel(L, sampler.get_C())

signal_queue = ss.multiprocessing.SafeQueue()
detection_queue = ss.multiprocessing.SafeQueue()

websocket_src_queue = ss.multiprocessing.SafeQueue()
websocket_rec_queue = ss.multiprocessing.SafeQueue()
websocket_det_queue = ss.multiprocessing.SafeQueue()

num = 1000
t = time.time()
for i in range(num):
    inp = source.generate(block_size)
    sam = sampler.sample(inp)
    out = reconstructor.reconstruct(sam)
total = time.time() - t
print "non mp", total / num

p1 = Process(target=pr.run_generator,
             args=(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor))
p2 = Process(target=pr.run_reconstructor,
             args=(signal_queue, websocket_rec_queue, detection_queue, reconstructor, sample_freq))
proc = [p1, p2]
[p.start() for p in proc]
[p.join() for p in proc]
