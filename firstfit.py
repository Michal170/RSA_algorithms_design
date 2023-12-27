from xml.sax import parseString
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
        self.slots = np.zeros((len(paths), max_slot))
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
                out = None

                # Tutaj mamy wszystkie 30 proponowanych ścieżek wraz z bitratem
                for p in path:
                    distance = np.sum(self.distances[p == 1])
                    path_idx = np.where(p == 1)[0]
                    num_slots = self.choose_slots_num(distance, demand.bitrates[i])
                    out = self._allocate_slots(num_slots, path_idx)
                    if out == True:
                        break

                if out == False:
                    self.blocked += 1
                
            print(f"Demands: {len(self.demands)}")
            print(f"Blocked Count: {self.blocked}")
            print(f"Blocked Ratio: {self.blocked/len(self.demands)}")
            exit("END...")
                

    def _allocate_slots(self, num_slots: int, path_idx: np.array) -> bool:
        """Allocate slots"""
        slots = np.bitwise_or.reduce(self.slots[path_idx].astype(int), axis=0)
        idx = np.where(np.convolve(slots, np.ones(num_slots), mode='valid') == 0)[0]

        if idx.size == 0:
            return False
        else:
            start_idx = idx[0]
            self.slots[path_idx, start_idx:start_idx + num_slots] = 1
            return True

    def _release_slots(self):
        pass

if __name__ == "__main__":
    demands = load_demands("POL12/demands_6")
    paths = load_paths("POL12/pol12.pat")
    xd = FirstFit(demands=demands, paths=paths, distances=distances)
    xd.find_path()
    