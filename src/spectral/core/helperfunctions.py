import numpy as np
import scipy as sp
import scipy.signal


def signal_power(signal):
    """ Calculates the signal power of a signal by
    P = |signal|^2/len

    args:
        signal: Input signal.

    returns:
        The power of the signal.
        """
    return np.linalg.norm(signal) ** 2 / len(signal)


def hermitian(array):
    """
    Calculates the Hermitian of a matrix.

    args:
        array: The input matrix.
    returns:
        The Hermitian of the input matrix.
    """
    return np.conjugate(np.transpose(array))

def fft(signal):
    """
    Calculates the fast Fourier transform of the given signal,
    shifts it and returns its absolute value.

    args:
        signal: The input signal.
    returns:
        The absolute value the shifted FFT.
    """
    return np.abs(np.fft.fftshift(np.fft.fft(signal)))


def convert_db(value):
    """
    Converts the given value to decibels.

    args:
        value: The value to convert.
    returns:
        The resulting value in decibels.
    """
    return 10 * np.log10(value)


def invert_db(value):
    """
    Converts the given value in decibels back to a linear scale.

    args:
        value: The value in decibels to convert.
    returns:
        The resulting value.
    """
    return 10 ** (value / 10.0)


def psd(signal):
    """
    Calculates the power spectral density of the input signal.

    args:
        signal: The input signal.
    returns:
        The power spectral density of the signal.
    """
    return fft(auto_correlation(signal))


def remove_bias(signal):
    """
    Removes triangular windows from correlated signals.

    args:
        signal: The input signal.
    returns:
        The resulting signal.
    """
    window = sp.signal.triang(len(signal))
    window = window / min(window)
    return signal / window


def add_bias(signal):
    """
    Adds triangular windows to correlated signals.

    args:
        signal: The input signal.
    returns:
        The resulting signal.
    """
    window = sp.signal.triang(len(signal))
    window = window / min(window)
    return signal * window


def cross_correlate(a, b, maxlag=None, unbiased=True):
    """
    Cross correlates two signals with the set maximum of lags,
    if the unbiased flag is set to True, the bias is removed from the result
    before returning the result.

    args:
        a: The first signal to correlate.
        b: The second signal to correlate.
        maxlag: The maximum amount of lags to calculate.
        unbiased: Whether the resulting signal should be unbiased.
    returns:
        The correlated signal.
    """
    if len(a) != len(b):
        raise ValueError("a and b must be of same size.")
    size = len(a)
    cross_corr = sp.signal.fftconvolve(a, np.conj(b[::-1]), mode='full')

    if unbiased:
        cross_corr = remove_bias(cross_corr)

    if maxlag is not None:
        if not(1 <= maxlag < (size + 1)):
            raise ValueError("maxlag needs to be none or strictly positive and smaller than {}".format(size))
        cross_corr = cross_corr[size - maxlag - 1:size + maxlag]
    return cross_corr


def auto_correlation(signal, maxlag=None, unbiased=True):
    """
    Calculates the autocorrelation of the given signal
    with the set maximum of lags, if the unbiased flag is set to True,
    the bias is removed from the result before returning the result.

    args:
        signal: The input signal.
        maxlag: The maximum amount of lags to calculate.
        unbiased: Whether the resulting signal should be unbiased.
    returns:
        The correlated signal.
    """
    return cross_correlate(signal, signal, maxlag=maxlag, unbiased=unbiased)


CACHE_DIR = "cache/"
