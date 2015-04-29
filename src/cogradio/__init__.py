from . import sampling
from . import detection
from . import source
from . import reconstruction

import matplotlib.pyplot as plt
import numpy as np


def plot_fft(signal, samp_freq, window):
    fft = np.fft.fftshift(np.abs(np.fft.fft(signal)))
    freq = np.linspace(-samp_freq/2, samp_freq/2, samp_freq*window)
    plt.plot(freq, fft)
    plt.show()
