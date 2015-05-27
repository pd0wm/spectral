import cogradio_utils as cg

import cProfile
import pstats
import StringIO

N = 14
L = 40
frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 2.41e9
sample_freq = 10e6
multiplier = 100  # Warning: greatly diminishes perfomance
nyq_block_size = L * N * multiplier
window_length = nyq_block_size
threshold = 2000

pr = cProfile.Profile()
pr.enable()
source = cg.source.ComplexExponential(frequencies, sample_freq, SNR=5)
sampler = cg.sampling.MultiCoset(N)
reconstructor = cg.reconstruction.Wessel(N, L)
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
pr.dump_stats("Single_process_complete_init.dmp")


pr = cProfile.Profile()
pr.enable()
for i in range(100):
    signal = source.generate(nyq_block_size)
    cos_samp = sampler.sample(signal)
    rec_sig = reconstructor.reconstruct(cos_samp)
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
pr.dump_stats("Single_process_complete.dmp")
