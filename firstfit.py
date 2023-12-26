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
                # Tutaj mamy wszystkie 30 proponowanych ścieżek wraz z bitratem

                for p in path:
                    distance = 0
                    for d in range(len(p)):
                        if p[d] == 1:
                            distance += self.distances[d]

                    num_slots = self.choose_slots_num(distance, demand.bitrates[i])
                    out = self._allocate_slots(num_slots)
                    print(out)

                    if out:
                        break
                
                

                print(self.slots)
                print("\n")
                exit("Demands Testing ...")
            exit("Testing...")
                

    def _allocate_slots(self, num_slots: int) -> bool:
        """Allocate slots"""
        # Alokacja widma ale narazie nie uwzględnia 
        idx = np.where(np.convolve(self.slots, np.ones(num_slots), mode='valid') == 0)[0]
        if idx.size == 0:
            return False
        else:
            print(idx)
            start_idx = idx[0]
            print(f"Start index: {start_idx}")
            self.slots[start_idx:start_idx + num_slots] = 1
            return True

    def _release_slots(self):
        pass

if __name__ == "__main__":
    demands = load_demands("POL12/demands_0")
    paths = load_paths("POL12/pol12.pat")
    xd = FirstFit(demands=demands, paths=paths, distances=distances)
    xd.find_path()
    