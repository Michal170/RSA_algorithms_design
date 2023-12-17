import numpy as np

from helpers.import_data import load_paths
from helpers.import_data import load_demands
from demand import Demand
from helpers.distances import distances
from base import Base

"""
What is needed to store in this class
"""

class FirstFit(Base):
    def __init__(self, paths: np.ndarray, distances: np.array, demands: np.ndarray, max_slot=320, node_num: int = 12):
        super().__init__(node_num=node_num)
        self.paths = paths
        self.distances = distances
        self.slots = np.zeros(max_slot)
        self.bitrates_num = demands.shape[1] - 3
        self.blocked = 0
        self.demands = []
        for i in demands:
            self.demands.append(Demand(i))
        self.demands = np.array(self.demands)
        
    def find_path(self):
        for i in range(self.bitrates_num):
            for demand in self.demands:
                idx = self.nodes_mapping(demand.node_in, demand.node_out)
                path = self.paths[idx]
                # Tutaj mamy wszystkie 30 proponowanych ścieżek wraz z bitratem

                for p in path:
                    for d in range(len(p)):
                        if p[d] == 1:
                            distance = self.distances[d]
                            num_slots = self.choose_slots_num(distance, demand.bitrates)



                    print(p)
                print("\n")


    def _release_slots(self):
        pass

    def _allocate_slots(self):
        pass

if __name__ == "__main__":
    demands = load_demands("POL12/demands_0")
    paths = load_paths("POL12/pol12.pat")
    xd = FirstFit(demands=demands, paths=paths, distances=distances)
    xd.find_path()
    