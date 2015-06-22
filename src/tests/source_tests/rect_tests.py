import unittest
import numpy as np
import spectral.core as sc
import matplotlib.pyplot as plt

class SinusoidalTests(unittest.TestCase):
    def setUp(self):
        self.freqs = [100, 200, 300]
        self.width = 10
        self.widths = [self.width] * 3
        self.samp_freq = 1000

    def no_snr_rect_test(self):
        expected_complex_freqs = [200, 300, 400, 600, 700, 800]
        delta = 50
        source = sc.source.Rect(self.freqs, self.widths, self.samp_freq)

        samples = source.generate(self.samp_freq)
        fft = np.abs(np.fft.fftshift(np.fft.fft(samples)))

        for i, v in enumerate(fft):
            print i, v
            for f in expected_complex_freqs:
                if np.abs(f - i) < self.width - 1:
                    self.assertGreater(v, delta)
