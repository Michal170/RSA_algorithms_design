import sys
import numpy as np
from helpers.path_names import paths_names

def import_distances(path: str) -> np.array:
    data = np.loadtxt(path, dtype=int).flatten() 
    distances = data[data != 0]
    return np.array(distances)

# Creates distances releated to path_names
# It is possible to import them 
sys.path.insert(0, '../')
distances = import_distances("POL12/pol12.net")
