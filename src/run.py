import cogradio as cg
import numpy as np
import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt
np.set_printoptions(linewidth=800,
                    edgeitems=20)

frequencies = [0.24, 0.11, 0.35, 0.45]
widths = [1e3, 5e3]
snr = 0
L = 50
N = 14
nyq_block_size = L * N
f_samp = 1
M = 6
window = L*N
numbbins = 15

source = cg.source.Sinusoidal(frequencies, SNR=snr).generate(f_samp, window)
print "Source shape " + str(source.shape)

sampler = cg.sampling.MultiCoset(N)
multicos_signal = sampler.sample(source)
print "mc_signal shape " + str(multicos_signal.shape)
# print "mc_signal\n" + str(multicos_signal.transpose())

reconstructor = cg.reconstruction.CrossCorrelation(N, M, sampler.get_C(), L)
rx = reconstructor.reconstruct(multicos_signal.transpose())

y_s = cg.fft(rx)
binwidth = np.round(y_s.shape[0] / numbbins)
y_avgd = np.zeros((y_s.shape[0]))
for i in range(0, y_s.shape[0], binwidth):
    y_avgd[i:i+binwidth] = np.mean(y_s[i:i+binwidth])

print y_avgd

plt.figure(1)
plt.subplot(211)
rx_len = (rx.shape[0])
f_axis_recon = np.linspace(-0.5, 0.5, rx_len)
plt.stem(f_axis_recon, y_avgd)
plt.plot(f_axis_recon, y_s)

print "autocorr length = " + str(rx.shape)

plt.subplot(212)
plt.stem(np.linspace(-0.5, 0.5, source.shape[0]), cg.psd(source))
plt.show()
