from . import sampling
from . import detection
from . import source
from . import reconstruction

import matplotlib.pyplot as plt
import numpy as np

def signal_power(signal):
    return np.linalg.norm(signal)**2 / len(signal)

def plot(signal):
    plt.plot(signal)
    plt.show()

def plot_fft(signal, samp_freq, window):
    fft = np.fft.fftshift(np.abs(np.fft.fft(signal)))
    freq = np.linspace(-samp_freq/2, samp_freq/2, samp_freq*window)
    plt.plot(freq, fft)
    plt.xlabel("f")
    plt.ylabel("|x|")
    plt.show()
