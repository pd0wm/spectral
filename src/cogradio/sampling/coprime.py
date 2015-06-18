from .multicoset import MultiCoset


class Coprime(MultiCoset):

    """Coprime coset sampler implementation"""

    def __init__(self, a, b):
        self.a = a
        self.b = b
        intervals = self.coprime_multiples(a, b)
        N = a * b
        M = a + b - 1
        super(Coprime, self).__init__(intervals, N, M)

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
