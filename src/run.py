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
reconstructor = cg.reconstruction.Wessel(N,L)
detector = cg.detection.SPFL();

plt.figure(1)

ax = plt.subplot(121)
ax2 = plt.subplot(122)

nyq_signal = source.generate(f_samp, window)
mc_signal = sampler.sample(nyq_signal)
rx = reconstructor.reconstruct(mc_signal)

y_s = cg.fft(rx)

# Axis generation
rx_len = (rx.shape[0])
detected = detector.detect(rx, len(rx)/numbins, 4E-8)

f_axis_recon = np.linspace(-0.5, 0.5, rx_len)

ax.plot(cg.psd(nyq_signal))
ax2.plot(f_axis_recon, y_s)
plt.show()