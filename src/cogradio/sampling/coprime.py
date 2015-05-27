import numpy as np
import cogradio as cg
from .sampling import Sampler


class Coprime(Sampler):

    """Coprime coset sampler implementation"""

    def __init__(self, a, b, mode="cps"):
        Sampler.__init__(self)
        self.a = a
        self.b = b
        self.C = self.generate_C()

    def sample(self, signal):
        chunk_size = self.a * self.b
        output_chunk_size = self.a + self.b - 1
        chunks = int(np.floor(len(signal) / chunk_size))
        output = np.zeros((output_chunk_size  * chunks))
        for i, j in zip(range(0, chunks*output_chunk_size, output_chunk_size), (range(0, chunks * chunk_size, chunk_size))):
             output[i:i + output_chunk_size] = np.dot(signal[j:j + chunk_size], self.C)
        return output

    def generate_C(self):
        n = range(max(self.a, self.b))  # max number of multiples in the coprime solution
        C = np.zeros((self.a * self.b, self.a + self.b - 1))

        a_indices = {i * self.a for i in n if i * self.a < self.a * self.b}
        b_indices = {i * self.b for i in n if i * self.b < self.a * self.b}
        indices = list(a_indices.union(b_indices))

        for j, i in enumerate(indices):
            C[i, j] = 1
        return C
