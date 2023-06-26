import numpy as np


def normalize_data(data):
    data_norm = data.div(data.sum(axis=0), axis=1) * 1e6
    data_norm = data_norm.transform(np.log1p)
    data_norm = data_norm.loc[data_norm.sum(axis=1) > 3]
    return data_norm
