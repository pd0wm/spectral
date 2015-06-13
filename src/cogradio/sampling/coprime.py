import numpy as np
from .sampling import Sampler


class Coprime(Sampler):

    """Coprime coset sampler implementation"""

    def __init__(self, a, b):
        Sampler.__init__(self)
        self.a = a
        self.b = b
        self.C = self.generate_C()
        self.N = self.C.shape[1]

    def sample(self, x):
        length = x.shape[0]
        offset = length % self.N
        if offset != 0:
            x = x[:-offset]
        x = np.reshape(x.T, (self.N, -1), order='F')
        y = np.dot(self.C, x)
        return y

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
