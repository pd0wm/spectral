import numpy as np
import cogradio as cg
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

    def cross_correlation_signals(self, signal):
        Ry = np.zeros((self.M ** 2, 2 * self.L - 1), dtype=np.complex64)
        for i in range(self.M):
            for j in range(self.M):
                Ry[i * self.M + j] = cg.cross_correlate(signal[i, :],
                                                        signal[j, :],
                                                        maxlag=self.L - 1)
        return Ry

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
            return False
        Mat_accent = Mat.dot(Pinv.dot(Mat))
        check = np.allclose(Mat_accent.toarray(), Mat.toarray(), atol=1e-5)
        return check

    def get_non_zero_column(self, matrix):
        return set(np.nonzero(matrix)[1])  # Vieze oneliners ftw

    def get_filename(self):
        filepath = cg.CACHE_DIR
        filename = self.__class__.__name__
        filename += str(self.L) + "_"
        filename += "_".join(str(rule) for rule in self.get_non_zero_column(self.C))
        return filepath + filename
