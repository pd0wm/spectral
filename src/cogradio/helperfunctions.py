import numpy as np
import scipy.signal


def signal_power(signal):
    return np.linalg.norm(signal) ** 2 / len(signal)


def fft(signal):
    return np.abs(np.fft.fftshift(np.fft.fft(signal)))


def freq_axis(samp_freq, duration):
    return np.linspace(-samp_freq / 2, samp_freq / 2, samp_freq * duration)


def time_axis(samp_freq, duration):
    return np.linspace(0, duration, duration * samp_freq)


def convert_db(value):
    return 10 * np.log10(value)


def invert_db(value):
    return 10 ** (value / 10.0)


def psd(signal):
    return fft(auto_correlation(signal))


def cross_correlate(a, b, maxlag=None):
    if len(a) != len(b):
        raise ValueError("a and b must be of same size.")

    size = len(a)
    cross_corr = scipy.signal.fftconvolve(a, np.conj(b[::-1]), mode='full')

    if maxlag is not None:
        if not(1 < maxlag < (size + 1)):
            raise ValueError("maglag needs to be none or strictly positive and smaller then {}".format(size))
        return cross_corr[size - maxlag - 1:size + maxlag]
    else:
        return cross_corr


def auto_correlation(signal):
    return np.correlate(signal, signal, mode='same')


def build_sparse_ruler_sampling_matrix(sparseruler, N):
    M = len(sparseruler)
    C = np.zeros((M, N))
    for i in range(0, M):
        C[i, sparseruler[i]] = 1
    return C

CACHE_DIR = "cache/"
