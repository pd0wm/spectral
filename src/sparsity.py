import spectral.core as sc
import time
import numpy as np
import matplotlib.pyplot as plt
import cProfile, pstats, StringIO

def time_runs(matrix, M):
    runs = 1000
    vec = np.random.rand(matrix.R.shape[0])
    vec = vec.reshape((M, -1))
    t = time.time()
    for i in range(runs):
        matrix.reconstruct(vec)
    runtime = time.time() - t
    return runtime / runs

N = 6
L_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 50]
sample = sc.sampling.MinimalSparseRuler(N)
M = sample.get_C().shape[0]
sparse_times = []
numpy_times = []
no_elemts = []
for L in L_values:
    rec = sc.reconstruction.Wessel(L, sample.get_C())
    rec_2 = sc.reconstruction.Wessel(L, sample.get_C(), cache=False)
    sparse_mat = rec.R_pinv
    norm_mat = rec.get_Rpinv()
    no_elemts.append(norm_mat.shape[0] * norm_mat.shape[1])
    sparse_times.append(time_runs(rec, M))
    numpy_times.append(time_runs(rec_2, M))
print sparse_times
print numpy_times
dump = np.zeros((len(sparse_times), 3))
dump[:, 0] = no_elemts
dump[:, 1] = sparse_times
dump[:, 2] = numpy_times
np.savetxt("sparse.csv", dump, delimiter=',')
plt.plot(no_elemts, sparse_times)
plt.plot(no_elemts, numpy_times)
plt.show()
