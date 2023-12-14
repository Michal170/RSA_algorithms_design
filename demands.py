from dataclasses import dataclass
import numpy as np
from helpers.import_data import import_data
from helpers.distances import distances

class Edge(object):
    def __init__(self, node_in: int, node_out: int, bitrates: np.array):
        self.node_in = int(node_in)
        self.node_out = int(node_out)
        self.bitrates = bitrates

if __name__ == "__main__":
    # Just for testing purpose
    data = import_data("./POL12/demands_0")
    data = np.delete(data, 2, axis=1)
    arr_data = [Edge(data[x,0], data[x,1], data[x, 2:]) for x in range(len(data))]
    print(arr_data[0].node_in)
    print(distances)
