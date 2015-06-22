import spectral.core as sc
import cProfile

L = 3
a = 7
b = 11
N = 61
frequencies = [2e3, 4e3, 5e6, 8e6]
widths = [1000, 1000, 1000, 1000]
center_freq = 2.41e9
sample_freq = 10e6
multiplier = 100  # Warning: greatly diminishes perfomance
nyq_block_size = L * N * multiplier
window_length = nyq_block_size
threshold = 2000
runs = 1000


def gen_profiling_report(obj, args, runs, method=None, constructor=False):
    pr = cProfile.Profile()
    pr.enable()
    for i in range(runs):
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

if __name__ == "__main__":
    sources = [sc.source.Sinusoidal, sc.source.ComplexExponential, sc.source.Rect]
    sources_init_args = [(frequencies, sample_freq)] * 2
    sources_init_args.append((frequencies, widths, sample_freq))
    init_sources = []
    for obj, args in zip(sources, sources_init_args):
        init_sources.append(gen_profiling_report(obj, args, runs, obj, constructor=True))

    init_samplers = []
    samplers = [sc.sampling.Coprime, sc.sampling.MultiCoset]
    sampler_init_args = [(a, b), (N,)]

    for obj, args in zip(samplers, sampler_init_args):
        init_samplers.append(gen_profiling_report(obj, args, runs, obj, constructor=True))

    C = init_samplers[1].get_C()

    reconstructors = [sc.reconstruction.CrossCorrelation, sc.reconstruction.Wessel]
    reconstructors_init_args = [(L, C, False)] * len(reconstructors)

    init_reconstructors = []
    for obj, args in zip(reconstructors, reconstructors_init_args):
        init_reconstructors.append(gen_profiling_report(obj, args, runs, obj, constructor=True))

    sources_gen_args = [(nyq_block_size,)] * len(init_sources)
    signals = []
    for obj, args in zip(init_sources, sources_gen_args):
        signals.append(gen_profiling_report(obj, args, runs, obj.generate))

    sample_samp_args = [(signals[0],)] * len(init_samplers)
    sampled_signal = []
    for obj, args in zip(init_samplers, sample_samp_args):
        sampled_signal.append(gen_profiling_report(obj, args, runs, obj.sample))

    reconst_reconstr_args = [(sampled_signal[1],)] * len(reconstructors)
    reconstr_signal = []
    for obj, args in zip(init_reconstructors, reconst_reconstr_args):
        reconstr_signal.append(gen_profiling_report(obj, args, runs, obj.reconstruct))
