#!/usr/bin/env python
import cogradio as cg
import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt
np.set_printoptions(linewidth=800, edgeitems=20, threshold=100)

frequencies = [0.3421, 0.3962, 0.1743, 0.1250];
L = 50
N = 14
nyq_block_size = L * N
f_samp = 1
M = 6
window = (L + 1) * N
numbbins = 15

# print "Compression", float(M)/N

source = cg.source.Sinusoidal(frequencies).generate(f_samp, window)
# print "Source shape " + str(source.shape)
#np.savetxt("py_source.tmp", source, delimiter=',')

sampler = cg.sampling.MultiCoset(N)
multicos_signal = sampler.sample(source)
print multicos_signal.shape
# print "mc_signal shape " + str(multicos_signal.shape)
#np.savetxt("py_mc.tmp", multicos_signal, delimiter=',')

reconstructor = cg.reconstruction.CrossCorrelation(N, M, sampler.get_C(), L)
rx = reconstructor.reconstruct(multicos_signal)

detector = cg.detection.CAV()
detector.detect(rx)

y_s = cg.fft(rx)
binwidth = np.round(y_s.shape[0] / numbbins)
y_avgd = np.zeros((y_s.shape[0]))
for i in range(0, y_s.shape[0], binwidth):
    y_avgd[i:i+binwidth] = np.mean(y_s[i:i+binwidth])

# print y_avgd

plt.figure(1)
plt.subplot(211)
rx_len = (rx.shape[0])
f_axis_recon = np.linspace(-0.5, 0.5, rx_len)
plt.stem(f_axis_recon, y_avgd)
plt.stem(f_axis_recon, y_s)

# print "autocorr length = " + str(rx.shape)

plt.subplot(212)
plt.stem(np.linspace(-0.5, 0.5, source.shape[0]), cg.psd(source))
plt.show()

#np.savetxt("py_rx.tmp", rx, delimiter=',')
