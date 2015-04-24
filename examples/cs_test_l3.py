from scipy import signal, linalg
import numpy as np
import matplotlib.pyplot as plt
import random
import cvxopt

samp_freq = 50e3               #hz
duration = 0.01                 #s
input_signal = np.array([])
frequencies = [10e3, 15e3, 25e3]

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

rand_values = [0]

while len(rand_values) < meas_length:
    rand_values.append(rand_values[-1] + random.randrange(3, 6))

# rand_values = sorted(random.sample(range(0, input_length), meas_length))

for m, n in enumerate(rand_values):
    sample_matrix[m, n] = 1;

sample_matrix = np.matrix(sample_matrix)
y = meas_signal = (sample_matrix * np.matrix(input_signal).T)
b =  np.concatenate((y, np.array([[0], [0]])))
F_inv = linalg.inv(linalg.dft(input_length))
samp_F_inv = sample_matrix * F_inv

rec_signal = np.matrix(np.linalg.pinv(sample_matrix)) * np.matrix(meas_signal)

plt.subplot(2, 1, 1)
plt.plot(np.abs(np.fft.fftshift(np.fft.fft(input_signal.T)).T))
plt.subplot(2, 1, 2)
plt.plot(np.abs(np.fft.fftshift(np.fft.fft(rec_signal.T)).T))
plt.show()
