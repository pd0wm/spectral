#!/usr/bin/env python
import cogradio_utils as cg
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from time import sleep
import os


np.set_printoptions(linewidth=800, edgeitems=20, threshold=100)

frequencies = [0.3421, 0.3962, 0.1743, 0.1250]
L = 20
N = 14
nyq_block_size = L * N
f_samp = 1
window = L * N
numbins = 15
threshold = 2000

# Init blocks
source = cg.source.ComplexExponential(frequencies, SNR=0)
sampler = cg.sampling.MultiCoset(N)
C = sampler.generateC()
#reconstructor = cg.reconstruction.CrossCorrelation(N, L, C)
reconstructor2 = cg.reconstruction.Wessel(N,L)

#reconstructor2.reconstruct(None)
# Compressive sensing
nyq_signal = source.generate(f_samp, window)
fp  = open("/home/twiel/ofdm.dmp")
fp.seek(0, os.SEEK_END)
size = fp.tell()

fp.seek(1024*1024*10)

# nyq_signal = sp.fromfile(fp, dtype=sp.complex64, count=window)
mc_signal = sampler.sample(nyq_signal)
rx = reconstructor2.reconstruct(mc_signal)
print("Nu de rx shit")
print(rx.shape)
y_s = cg.fft(rx)
print(abs(y_s))

    # Axis generation
rx_len = (rx.shape[0])
f_axis_recon = np.linspace(-0.5, 0.5, rx_len)

plt.figure(1)
plt.subplot(211)
plt.plot(f_axis_recon, y_s)

plt.subplot(212)
plt.stem(np.linspace(-0.5, 0.5, nyq_signal.shape[0]), cg.psd(nyq_signal))
plt.show()

