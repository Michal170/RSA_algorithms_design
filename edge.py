import numpy as np
from helpers.import_data import load_demands
from helpers.distances import distances

class Edge(object):
    def __init__(self, node_in: int, node_out: int, bitrates: np.array):
        self.node_in = int(node_in)
        self.node_out = int(node_out)
        self.bitrates = bitrates
