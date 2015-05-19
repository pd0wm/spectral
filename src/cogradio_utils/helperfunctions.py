import numpy as np


def signal_power(signal):
    return np.linalg.norm(signal) ** 2 / len(signal)


def fft(signal):
    fft = np.abs(np.fft.fftshift(np.fft.fft(signal)))
    return fft


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


def auto_correlation(signal):
    return np.correlate(signal, signal, mode='same')


def build_C(sparseruler, N):
    M = len(sparseruler)
    C = np.zeros((M, N))
    for i in range(0, M):
        C[i, sparseruler[i]] = 1
    return C

CACHE_DIR = "cache/"
