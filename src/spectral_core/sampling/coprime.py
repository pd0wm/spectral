from .multicoset import MultiCoset


class Coprime(MultiCoset):

    """
    Coprime coset sampler implementation. Derives from the
    multi-coset class and implements its own (coprime) intervals.
    These intervals are based on two samplers with Fs1/Fs2 = a/b with
    a and b the coprime numbers.

    Args:
        a: First coprime number
        b: Second coprime number
    """

    def __init__(self, a, b):
        intervals = self.coprime_multiples(a, b)
        N = a * b
        M = a + b - 1
        super(Coprime, self).__init__(intervals, N, M)

    def coprime_multiples(self, a, b):
        """
        Generator function that generates a integer multiples
        of the coprime numbers starting with zero (in order of size)
        until all multiples smaller than a * b are returned

        Args:
            a: first coprime number
            b: second coprime number

        Yields:
            x in ((n*a) union (n*b)) for n in [0, 1, ...] and x < a * b
        """
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
