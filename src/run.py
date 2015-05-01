import cogradio as cg
import numpy as np
# import matplotlib.pyplot as plt


frequencies = [6e3, 20e3]
widths = [1e3, 5e3]
samp_freq = 100e3
window = 0.1
snr = 20
N = 5
M = 2
C = np.zeros((M, N))

a = cg.reconstruction.CrossCorrelation(N, M, C)
a.reconstruct([50, 2])
