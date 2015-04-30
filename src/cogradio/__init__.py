from . import sampling
from . import detection
from . import source
from . import reconstruction
import numpy as np


def signal_power(signal):
    return np.linalg.norm(signal)**2 / len(signal)


def fft(signal, samp_freq, window):
    fft = np.fft.fftshift(np.abs(np.fft.fft(signal)))
    freq = np.linspace(-samp_freq/2, samp_freq/2, samp_freq*window)
    return (freq, fft)


def convert_db(value):
    return 10*np.log10(value)


def invert_db(value):
    return 10**(value/10.0)
