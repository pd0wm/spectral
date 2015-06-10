import numpy as np
from .sampling import Sampler


class Coprime(Sampler):

    """Coprime coset sampler implementation"""

    def __init__(self, a, b):
        Sampler.__init__(self)
        self.a = a
        self.b = b
        self.C = self.generate_C()

    def sample(self, signal):
        chunk_size = self.a * self.b
        output_chunk_size = self.a + self.b - 1
        chunks = int(np.floor(len(signal) / chunk_size))
        output = np.zeros((output_chunk_size, chunks), dtype=np.complex64)

        for i, j in enumerate(range(0, chunks * chunk_size, chunk_size)):
            output[:, i] = np.dot(np.fliplr(self.C), signal[j:j + chunk_size])
        return output

    def generate_C(self):
        C = np.zeros((self.a + self.b - 1, self.a * self.b))
        for i, j in enumerate(self.coprime_multiples(self.a, self.b)):
            C[i, j] = 1
        return C

    def coprime_multiples(self, a, b):
        mult_a = a
        mult_b = b
        yield 0
        while min(mult_a, mult_b) < a * b:
            if (mult_a < mult_b):
                yield mult_a
                mult_a += a
            else:
                yield mult_b
                mult_b += b
