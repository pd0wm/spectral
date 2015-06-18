import cogradio as cg
import cProfile

N = 6
L = 40
a = 2
b = 3
frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 2.41e9
sample_freq = 10e6
multiplier = 100  # Warning: greatly diminishes perfomance
nyq_block_size = L * N * multiplier
window_length = nyq_block_size
threshold = 2000


def gen_profiling_report(obj, args, method=None, constructor=False):
    pr = cProfile.Profile()
    pr.enable()
    ret = method(*args)

    pr.disable()
    # s = StringIO.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    if constructor:
        pr.dump_stats("profiler_reports/{}_{}.prof".format(obj.__name__, "init"))
    else:
        pr.dump_stats("profiler_reports/{}_{}.prof".format(obj.__class__.__name__, method.__name__))
    return ret


sources = [cg.source.Sinusoidal, cg.source.ComplexExponential]  # , cg.source.Rect]
sources_init_args = [(frequencies, sample_freq)] * len(sources)

init_sources = []
for obj, args in zip(sources, sources_init_args):
    init_sources.append(gen_profiling_report(obj, args, obj, constructor=True))

init_samplers = []
samplers = [cg.sampling.Coprime, cg.sampling.MultiCoset]
sampler_init_args = [(a, b), (N,)]

for obj, args in zip(samplers, sampler_init_args):
    init_samplers.append(gen_profiling_report(obj, args, obj, constructor=True))

C = init_samplers[0].get_C()

reconstructors = [cg.reconstruction.CrossCorrelation, cg.reconstruction.Wessel]
reconstructors_init_args = [(L, C)] * len(reconstructors)

init_reconstructors = []
for obj, args in zip(reconstructors, reconstructors_init_args):
    init_reconstructors.append(gen_profiling_report(obj, args, obj, constructor=True))

sources_gen_args = [(nyq_block_size,)] * len(init_sources)
signals = []
for obj, args in zip(init_sources, sources_gen_args):
    signals.append(gen_profiling_report(obj, args, obj.generate))


