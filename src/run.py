import cogradio
import numpy as np

frequencies = [100e3]
samp_freq = 300e3
window = 0.1
snr = -20


sig = cogradio.source.Sinusoidal(frequencies, SNR=snr)
samps = sig.generate(samp_freq, window)
cogradio.fft(samps, samp_freq, window)
