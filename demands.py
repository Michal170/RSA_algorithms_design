import numpy as np
from helpers.import_data import import_data

class Edge(object):
    def __init__(self, node_in: int, node_out: int, bitrates: np.array) -> None:
        self.node_in = node_in
        self.node_out = node_out
        self.bitrates = bitrates
    

if __name__ == "__main__":
    d = Edge()
    d.node_in