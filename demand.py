import numpy as np
from helpers.import_data import load_demands
from helpers.distances import distances

class Demand(object):
    def __init__(self, demand: np.ndarray):
        self.node_in = int(demand[0])
        self.node_out = int(demand[1])
        self.bitrates = demand[3:]
