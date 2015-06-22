import cProfile, pstats, StringIO
import spectral.core as sc
import numpy as np

L = 50
N = 10
sam = sc.sampling.MinimalSparseRuler(N)
M = sam.get_C().shape[0]
rec = sc.reconstruction.Wessel(L, sam.get_C())

vec = np.random.rand(rec.R_pinv.shape[1])
vec = vec.reshape((M, -1))
pr = cProfile.Profile()
pr.enable()
for i in range(100):
    rec.reconstruct(vec)
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
