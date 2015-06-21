import itertools

ruler = [0, 15, 17, 19, 21, 22, 29]
N = 30

double_ruler = ruler + [r + max(ruler) + 1 for r in ruler]
pairs = itertools.combinations(double_ruler, 2)
distances = set(map(lambda x: (max(x) - min(x)), pairs))
distances_up_to_n = distances & set(range(N))

if len(distances_up_to_n) == N - 1:
    print "OK M=", len(ruler)
else:
    print "Not OK"
