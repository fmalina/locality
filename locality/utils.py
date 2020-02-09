import numpy as np


def reject_outliers(data, m=1.2):
    """
    Any outlying elements removed based on some assumed distribution of the points.

    >>> reject_outliers([0, 32, 34, 35, 36, 89])
    [32, 34, 35, 36]
    >>> reject_outliers([29, 32, 34, 35, 36, 45])
    [32, 34, 35, 36]
    >>> reject_outliers([20, 32, 34, 35, 36, 45, 120, 126])
    [20, 32, 34, 35, 36, 45]
    """
    u = np.mean(data)
    s = np.std(data)
    return [e for e in data if (u - m * s < e < u + m * s)]
