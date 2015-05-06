def sparseruler(i):
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
        29: (0, 1, 2, 14, 18, 21, 24, 27, 29)
    }
    if (i - 1) > 19:
        raise NotImplementedError("Values higher than 19 not supported")
    return sparseruler[i - 1]
