#!/usr/bin/env python
import cogradio_utils as cg
import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt
np.set_printoptions(linewidth=800, edgeitems=20, threshold=100)

frequencies = [0.3421, 0.3962, 0.1743, 0.1250]
L = 50
N = 14
nyq_block_size = L * N
f_samp = 1
window = (L + 1) * N
numbbins = 15
threshold = 2000

# Init blocks
source = cg.source.Sinusoidal(frequencies, SNR=-5)
sampler = cg.sampling.MultiCoset(N)
reconstructor = cg.reconstruction.CrossCorrelation(N, L)

# Compressive sensing
nyq_signal = source.generate(f_samp, window)
mc_signal = sampler.sample(nyq_signal)
rx = reconstructor.reconstruct(mc_signal)
y_s = cg.fft(rx)

# Axis generation
rx_len = (rx.shape[0])
f_axis_recon = np.linspace(-0.5, 0.5, rx_len)

# Detection 
detector = cg.detection.SPFL()
detector.detect(rx)

# Plotting
# Reconstruction
plt.figure(1)
plt.subplot(211)
plt.stem(f_axis_recon, y_s)

# Original
plt.subplot(212)
plt.stem(np.linspace(-0.5, 0.5, nyq_signal.shape[0]), cg.psd(nyq_signal))
plt.show()
