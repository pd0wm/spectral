import spectral.core as sc
import spectral.supervisor as ss
from multiprocessing import Process
import time

dump_file_path = 'dumps/ofdm.dmp'
L = 3
N = 51
upscale_factor = 2000  # Warning: greatly diminishes performance
sample_freq = 10e6
block_size = N * upscale_factor * L
source = sc.source.File(dump_file_path)
sampler = sc.sampling.MinimalSparseRuler(N)
reconstructor = sc.reconstruction.Wessel(L, sampler.get_C())


def signalgen(source, sampler, queue):
    while True:
        inp = source.generate(block_size)
        sam = sampler.sample(inp)
        queue.queue(sam)


def reconstruct(recon, queue):
    inp = 0
    num = 1000
    t = time.time()
    while True:
        sam = queue.dequeue()
        if inp == num:
            total = time.time() - t
            print "mp", total / num
        if sam is not None:
            inp += 1
            out = reconstructor.reconstruct(sam)



signal_queue = ss.multiprocessing.SafeQueue()

num = 1000
t = time.time()
for i in range(num):
    inp = source.generate(block_size)
    sam = sampler.sample(inp)
    out = reconstructor.reconstruct(sam)
total = time.time() - t
print "non mp", total / num

p1 = Process(target=signalgen,
             args=(source, sampler, signal_queue,))

p2 = Process(target=reconstruct,
             args=(reconstructor, signal_queue,))
proc = [p1, p2]
[p.start() for p in proc]
[p.join() for p in proc]
