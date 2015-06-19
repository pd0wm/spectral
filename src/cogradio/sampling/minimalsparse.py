from .multicoset import MultiCoset


class MinimalSparseRuler(MultiCoset):

    """ Minimimal sparse ruler sampler. Generates a minimal sparse ruler
    and feeds it into the multicoset constructor.

    Args:
        N: Downsampling factor
    """

    def __init__(self, N):
        sparseruler = self.sparseruler(N)
        M = len(sparseruler)
        super(MinimalSparseRuler, self).__init__(sparseruler, N, M)

    def sparseruler(self, ruler_length):
        """ Lookup table for sparse ruler solutions.

        Args:
            ruler_length: Length of the ruler to be solved.

        Returns:
            Returns solution to minimal sparse ruler problem.
        """
        sparseruler = {
            1: (0, 1),
            2: (0, 1, 2),
            3: (0, 1, 3),
            4: (0, 1, 2, 4),
            5: (0, 1, 2, 5),
            6: (0, 1, 4, 6),
            7: (0, 1, 2, 3, 7),
            8: (0, 1, 2, 5, 8),
            9: (0, 1, 2, 6, 9),
            10: (0, 1, 2, 3, 6, 10),
            11: (0, 1, 2, 3, 7, 11),
            12: (0, 1, 2, 3, 8, 12),
            13: (0, 1, 2, 6, 10, 13),
            14: (0, 1, 2, 3, 4, 9, 14),
            15: (0, 1, 3, 6, 10, 14, 15),
            16: (0, 1, 2, 3, 8, 12, 16),
            17: (0, 1, 2, 3, 8, 13, 17),
            18: (0, 1, 4, 7, 10, 13, 16, 18),
            19: (0, 1, 2, 3, 4, 9, 14, 19),
            23: (0, 1, 2, 11, 15, 18, 21, 23),
            29: (0, 1, 2, 14, 18, 21, 24, 27, 29),
            50: (0, 1, 7, 9, 12, 31, 35, 45),
            60: (0, 1, 4, 6, 10, 22, 30, 37, 48)
        }
        if (ruler_length - 1) not in sparseruler:
            raise NotImplementedError("Values other than " + str(sparseruler.keys()) + " not implemented.")
        return sparseruler[ruler_length - 1]
