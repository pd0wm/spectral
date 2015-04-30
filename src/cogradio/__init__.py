from . import sampling
from . import detection
from . import source
from . import reconstruction

def signal_power(signal):
    return np.linalg.norm(signal)**2 / len(signal)

def plot(signal):
    plt.plot(signal)
    plt.show()

def floor_int_array(array):
    return int(np.floor(np.min(array)))

def ceil_int_array(array):
    return int(np.ceil(np.max(array)))

def fft(signal, samp_freq, window):
    fft = np.fft.fftshift(np.abs(np.fft.fft(signal)))
    freq = np.linspace(-samp_freq/2, samp_freq/2, samp_freq*window)
    return (freq, fft)
