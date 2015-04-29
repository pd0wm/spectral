from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import random

samp_freq = 100e3                 #hz
duration = 0.05                 #s
input_signal = np.array([])
frequencies = [25e3, 30e3, 10e3]

# Generate input signal
for f in frequencies:
    t = np.arange(0, np.ceil(duration * samp_freq)) / samp_freq
    sig = np.sin(2 * np.pi * f * t)
    input_signal = np.append(input_signal, sig)

# plt.specgram(input_signal)
# plt.show()

input_length = len(input_signal)
print input_length
meas_length = input_length / 10;
sample_matrix = np.zeros((meas_length, input_length))

rand_values = sorted(random.sample(range(0, input_length), meas_length))

for m, n in enumerate(rand_values):
    sample_matrix[m, n] = 1;

sample_matrix = np.matrix(sample_matrix)
meas_signal = (sample_matrix * np.matrix(input_signal).T)

rec_signal = np.matrix(np.linalg.pinv(sample_matrix)) * np.matrix(meas_signal)

plt.subplot(2, 1, 1)
plt.plot(np.abs(np.fft.fftshift(np.fft.fft(input_signal.T)).T))
plt.subplot(2, 1, 2)
plt.plot(np.abs(np.fft.fftshift(np.fft.fft(rec_signal.T)).T))
plt.show()
