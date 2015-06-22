import spectral.core as sc
import time
import numpy as np
import matplotlib.pyplot as plt


def time_runs(matrix):
    vec = np.ones(matrix.shape[1])
    t = time.time()
    for i in range(100):
        matrix.dot(vec)
    runtime = time.time() - t
    return runtime

N = 10
L_values = [1, 10, 20, 50, 200]
sample = sc.sampling.MinimalSparseRuler(N)
sparse_times = []
numpy_times = []
no_elemts = []
for L in L_values:
    rec = sc.reconstruction.Wessel(L, sample.get_C())
    sparse_mat = rec.R_pinv
    norm_mat = rec.get_Rpinv()
    print type(sparse_mat)
    print type(norm_mat)
    no_elemts.append(norm_mat.shape[0] * norm_mat.shape[1])
    sparse_times.append(time_runs(rec.R_pinv))
    numpy_times.append(time_runs(rec.get_Rpinv()))
print sparse_times
print numpy_times

plt.plot(no_elemts, sparse_times)
plt.plot(no_elemts, numpy_times)
plt.show()
