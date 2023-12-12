import numpy as np
import os

def import_data(demand_dir: str) -> np.array:
    """Import data from typed directory

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
    for d in dir:
        data.append(np.genfromtxt(os.path.join(demand_dir, d)))

    return np.array(data)