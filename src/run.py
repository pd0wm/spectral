import cogradio

frequencies = [10]
samp_freq = 250
window = 5


sig = cogradio.source.Sinusoidal(frequencies)
samps = sig.generate(samp_freq, window)
cogradio.plot_fft(samps, samp_freq, window)
