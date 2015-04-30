import cogradio
import numpy as np
import matplotlib.pyplot as plt

frequencies = [6e3, 20e3]
widths = [1e3, 5e3]
samp_freq = 100e3
window = 0.1
snr = 20


# sig = cogradio.source.Sinusoidal(frequencies, SNR=snr)
sig = cogradio.source.Rect(frequencies, widths)
samps = sig.generate(samp_freq, window)
# plt.plot(samps)
# plt.show()
# plt.cla()
signal_fft = cogradio.fft(samps, samp_freq, window)
# plt.plot(signal_fft[0], signal_fft[1])
# plt.show()
# autocor = cogradio.auto_correlation(samps)
# psd = cogradio.fft(autocor, samp_freq, window)
# plt.plot(psd[1])
# plt.show()
plt.plot(signal_fft[0], signal_fft[1])
plt.show()
