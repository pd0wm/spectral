import cogradio_utils as cg
import numpy as np
import scipy.sparse
import scipy as sp


class Reconstructor(object):

    """Parent class for reconstruction of spectrum sensed signal"""

    def __init__(self):
        pass

    def reconstruct(self, signal):
        raise NotImplementedError("Implement this method.")

    def get_filename(self):
        return (cg.CACHE_DIR + "wessel_cache_" + str(self.N) + str(self.L) + str(self.M))

    def cache_pseudoinverse(self, sparse):
        np.savez(self.get_filename(), data=sparse.data, indices=sparse.indices,
                 indptr=sparse.indptr, shape=sparse.shape)

    def load_pseudoinverse(self):
        try:
            loader = np.load(self.get_filename() + ".npz")
        except IOError:
            return None

        return sp.sparse.csr_matrix((loader['data'], loader['indices'],
                                     loader['indptr']), shape=loader['shape'])
