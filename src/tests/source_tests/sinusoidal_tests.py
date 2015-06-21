import unittest
import numpy as np
import spectral.core as sc


class SinusoidalTests(unittest.TestCase):
    def setUp(self):
        self.freqs = [100, 200, 300]

        self.samp_freq = 1000
        self.SNR = 10

    def no_noise_test(self):
        expected_complex_freqs = [200, 300, 400, 600, 700, 800]
        delta = 1e-6

        source = sc.source.Sinusoidal(self.freqs, self.samp_freq)
        samples = source.generate(self.samp_freq)
        fft = np.abs(np.fft.fftshift(np.fft.fft(samples)))

        for i, v in enumerate(fft):
            if i in expected_complex_freqs:
                self.assertGreater(v, delta)
            else:
                self.assertLess(v, delta)
