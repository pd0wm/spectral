import numpy as np
import spectral as spec
import scipy as sp


class Reconstructor(object):

    """Parent class for reconstruction of spectrum sensed signal"""

    def __init__(self):
        pass

    def get_Rpinv(self):
        """ Getter function for pinv.

        Returns:
            Returns the numpy representation of the R_pinv
        """
        return self.R_pinv.toarray()

    def reconstruct(self, signal):
        """
        Contract for the reconstruct method
        Raises:
            NotImplementedError
        """
        raise NotImplementedError("Implement this method.")

    def cache_pseudoinverse(self, sparse):
        """
        Caching function for the pseudoinverse

        Args:
            sparse: Sparse matrix to be cached.
        """
        np.savez(self.get_filename(), data=sparse.data, indices=sparse.indices,
                 indptr=sparse.indptr, shape=sparse.shape)

    def load_pseudoinverse(self):
        """
        Load the pseudoinverse from the cache.

        Returns:
            Sparse matrix from cache
        """
        try:
            loader = np.load(self.get_filename() + ".npz")
        except IOError:
            return None

        return sp.sparse.csr_matrix((loader['data'], loader['indices'],
                                     loader['indptr']), shape=loader['shape'])

    def cross_correlation_signals(self, signal):
        """
        Matrix style cross correlation calculation.
        Does a cyclic shift aswell as unbiasing the correlations.

        Args:
            signal: Input signal.
        returns
            Matrix of cross-correlations of the inputsignal.
        """
        length = signal.shape[1]
        max_lag = self.L - 1
        out = np.zeros((signal.shape[0] ** 2, 2 * self.L - 1), dtype=np.complex128)
        for lag in range(max_lag + 1):  # non-negative lags
            all_lags = np.dot(signal[:, lag:length], spec.core.hermitian(signal[:, :(length - lag)]))
            all_lags = all_lags.ravel(order='F') / float(length - lag)
            out[:, lag + max_lag] = all_lags
        for lag in range(max_lag + 1):  # non-positive lags
            all_lags = np.dot(signal[:, :length - lag], spec.core.hermitian(signal[:, lag:length]))
            all_lags = all_lags.ravel(order='F') / float(length - lag)
            out[:, max_lag - lag] = all_lags
        return out

    def calc_pseudoinverse(self, R):
        """
        Wrapper around scipy's pinv. Implements a caching mechanism.

        Args:
            R: Input R matrix
        Returns:
            R_pinv: inverse of said R matrix.
        """
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
        """
        Verifies if matrix is valid inverse of another matrix

        Args:
            mat: Matrix.
            Pinv: Potential inverse of said matrix.

        Returns:
            Bool which verifies if it is a valid pseudoinverse.
        """
        if Mat.shape != Pinv.shape[::-1]:
            return False
        Mat_accent = Mat.dot(Pinv.dot(Mat))
        check = np.allclose(Mat_accent.toarray(), Mat.toarray(), atol=1e-5)
        return check

    def get_non_zero_column(self, matrix):
        """
        Get the number of nonzero columns from the matrix.
        Unfortunate side effect of not having implicit access to the ruler
        that was used for the sampling matrix.

        Args:
            matrix: Matrix to be checked
        Returns:
            Set containing non zero colums.
        """
        return set(np.nonzero(matrix)[1])

    def get_filename(self):
        """
        Defines the filename for different input parameters.

        Returns:
            Filename which contains different input parameters and the name of
            the reconstructor used.
        """
        filepath = spec.core.CACHE_DIR
        filename = self.__class__.__name__
        filename += str(self.L) + "_"
        filename += "_".join(str(rule) for rule in self.get_non_zero_column(self.C))
        return filepath + filename
