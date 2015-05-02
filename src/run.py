import cogradio as cg
import numpy as np
# import matplotlib.pyplot as plt


frequencies = [6e3, 20e3]
widths = [1e3, 5e3]
samp_freq = 5e2
window = 0.1
snr = 20
N = 5
M = 2
C = np.zeros((M, N))

L = int(samp_freq*window/N)
print L

signal = np.random.rand(M, L)

a = cg.reconstruction.CrossCorrelation(N, M, C, samp_freq, L)
a.reconstruct(signal)
