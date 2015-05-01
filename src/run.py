import cogradio as cg
import numpy as np
import matplotlib.pyplot as plt

frequencies = [6e3, 20e3]
widths = [1e3, 5e3]
samp_freq = 100e3
window = 0.1
snr = 20


sig = cg.source.Rect(frequencies, widths)
samps = sig.generate(samp_freq, window)
signal_fft = cg.fft(samps)
