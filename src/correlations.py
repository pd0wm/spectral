import time
import numpy as np
import spectral.core as sc


def numpy_corr(a, b, maxlag=None, unbiased=True):
    cross_corr = np.correlate(a, b, mode='full')

    if unbiased:
        cross_corr = sc.remove_bias(cross_corr)

    return cross_corr

def fft_cross_corr(a):
    M = a.shape[0]
    L = a.shape[1]
    cross_correlations = np.zeros((M ** 2, 2 * L - 1),
                                  dtype=np.complex128)
    for i in range(0, M):
        for j in range(0, M):
            cross_correlations[i * M + j, :] = sc.cross_correlate(a[i], a[j])
    return cross_correlations


def cross_correlation_signals(signal):
    length = signal.shape[1]
    L = length
    max_lag = L - 1
    out = np.zeros((signal.shape[0] ** 2, 2 * L - 1), dtype=np.complex128)
    for lag in range(max_lag + 1):  # non-negative lags
        all_lags = np.dot(signal[:, lag:length], sc.hermitian(signal[:, :(length - lag)]))
        all_lags = all_lags.ravel(order='F') / float(length - lag)
        out[:, lag + max_lag] = all_lags
    for lag in range(max_lag + 1):  # non-positive lags
        all_lags = np.dot(signal[:, :length - lag], sc.hermitian(signal[:, lag:length]))
        all_lags = all_lags.ravel(order='F') / float(length - lag)
        out[:, max_lag - lag] = all_lags
    return out


def numpy_cross_corr(a):
    M = a.shape[0]
    L = a.shape[1]
    cross_correlations = np.zeros((M ** 2, 2 * L - 1),
                                  dtype=np.complex128)
    for i in range(0, M):
        for j in range(0, M):
            cross_correlations[i * M + j, :] = numpy_corr(a[i, :], a[j, :])
    return cross_correlations

def time_runs(vec, func):
    runs = 100
    t = time.time()
    for i in range(runs):
        res = func(vec)
    runtime = time.time() - t
    return runtime / runs



np_times = []
fft_times = []
mat_times = []

N = 10
lengths = np.linspace(1, 500, 100)
#lengths = [5]


for L in lengths:
    sam = sc.sampling.MinimalSparseRuler(N)
    orig = np.random.rand(L * N)
    inp = sam.sample(orig)
    np_times.append(time_runs(inp, numpy_cross_corr))
    fft_times.append(time_runs(inp, fft_cross_corr))
    mat_times.append(time_runs(inp, cross_correlation_signals))


print np_times
print fft_times
print mat_times
dump0 = np.zeros((len(np_times), 2))
dump0[:, 0] = lengths
dump0[:, 1] = np_times
np.savetxt("correlation0.csv", dump0, delimiter=',')

dump1 = np.zeros((len(np_times), 2))
dump1[:, 0] = lengths
dump1[:, 1] = fft_times
np.savetxt("correlation1.csv", dump1, delimiter=',')

dump2 = np.zeros((len(np_times), 2))
dump2[:, 0] = lengths
dump2[:, 1] = mat_times
np.savetxt("correlation2.csv", dump2, delimiter=',')
