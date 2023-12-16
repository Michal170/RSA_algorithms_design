import numpy as np

from helpers.import_data import load_paths
from helpers.import_data import load_demands
from helpers.distances import distances
from base import Base

"""
What is needed to store in this class
"""

class FirstFit(Base):
    def __init__(self, paths: np.ndarray, distances: np.array, demands: np.ndarray, slots_num=320, node_num: int = 12):
        super(FirstFit, Base).__init__(node_num=node_num)
        self.paths = paths
        self.distances = distances
        self.demands = demands
        self.slots = np.zeros(slots_num)
        
    def find_path(self):
        pass

    def _release_slots(self):
        pass

    def _allocate_slots(self):
        pass
    