import cogradio
import numpy as np
import matplotlib.pyplot as plt

frequencies = [100e3]
widths = [10e3]
samp_freq = 300e3
window = 0.1
snr = -20


# sig = cogradio.source.Sinusoidal(frequencies, SNR=snr)
sig = cogradio.source.Rect(frequencies, widths)
samps = sig.generate(samp_freq, window)
plt.plot(samps)
plt.show()
plt.cla()
signal_fft = cogradio.fft(samps, samp_freq, 2*window)
plt.plot(signal_fft[1])
plt.show()
