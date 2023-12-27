import numpy as np
import os


def load_demands(demand_dir: str) -> np.array:
    """
    Import data from typed directory

    Args:
        demand_dir (str): Directory where data are stored

    Returns:
        np.array: Data from directory

    Usage::

        from helpers.import_data import import_data

        dir="directory"
        X = import_data(dir)
    """

    data = []
    dir = os.listdir(demand_dir)
    dir = sorted(dir, key=lambda x: int(x.split(".")[0]))
    for d in dir:
        data.append(np.genfromtxt(os.path.join(demand_dir, d)))

    return np.array(data)


def load_paths(path: str) -> np.array:
    """
    Load proposed paths

    Args:
        path (str): Path to file with proposed paths

    Returns:
        np.array: Returns proposed paths
    """

    X = np.loadtxt(path, dtype=int)
    length = int(len(X) / 30)
    X = X.reshape((length, 30, 36))
    return np.array(X)
