import numpy as np


def roundLikeNCI(np_float64):
    outval = np.float64(np_float64) * np.float64(1000.0)
    if outval - outval.astype(np.int) >= np.float(0.5):
        outval = outval.astype(np.int) + 1
    else:
        outval = outval.astype(np.int)
    return np.float(outval) / np.float(1000)
