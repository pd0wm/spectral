import numpy as np
import scipy as sp


class Reconstructor(object):

    """Parent class for reconstruction of spectrum sensed signal"""

    def __init__(self):
        pass

    def reconstruct(self, signal):
        raise NotImplementedError("Implement this method.")

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

    def calc_pseudoinverse(self, R):
        R_pinv_accent = self.load_pseudoinverse()
        if R_pinv_accent is not None and self.check_valid_pinv(sp.sparse.csr_matrix(R), R_pinv_accent):
            print("Loaded reconstruction inversion matrix from file cache")
            R_pinv = R_pinv_accent
        else:
            print("Could not load from cache, rebuilding reconstruction inversion matrix")
            R_pinv = sp.sparse.csr_matrix(sp.linalg.pinv(R))
            self.cache_pseudoinverse(R_pinv)
        return R_pinv

    def check_valid_pinv(self, Mat, Pinv):
        if Mat.shape != Pinv.shape[::-1]:
            print "shapes dont align"
            return False
        Mat_accent = Mat.dot(Pinv.dot(Mat))
        check = np.allclose(Mat_accent.toarray(), Mat.toarray(), atol=1e-5)
        print "Matrix inv correct", check
        return check
