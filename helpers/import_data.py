import numpy as np
import os

def import_data(data_dir: str) -> np.array:
    """Import data from typed directory

    Args:
        data_dir (str): Directory where data are stored

    Returns:
        np.array: Data from directory
    
    Usage::

        from helpers.import_data import import_data

        dir="directory"
        X = import_data(dir)
    """    
    data = []
    dirs = os.listdir(data_dir)
    for i in dirs:
        if  os.path.isdir(os.path.join(data_dir, i)):
            d_part = []
            for d in os.listdir(os.path.join(data_dir, i)):
                d_part.append(np.genfromtxt(os.path.join(data_dir, i, d)))
            data.append(d_part)
            
    return np.array(data)