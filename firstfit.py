import numpy as np

from helpers.import_data import load_paths
from helpers.import_data import load_demands
from demand import Demand
from helpers.distances import distances
from base import Base

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
            for demand_idx, demand in enumerate(self.demands):
                idx = self.nodes_mapping(demand.node_in, demand.node_out)
                path = self.paths[idx]
                out = None

                for p in path:
                    distance = np.sum(self.distances[p == 1])
                    path_idx = np.where(p == 1)[0]
                    if i == 0:
                        num_slots = self.choose_slots_num(distance, demand.bitrates[i])
                        out = self._allocate_slots(num_slots, path_idx, demand_idx)
                        if out == True:
                                break

                    else:
                        num_slots_prev = self.choose_slots_num(distance, demand.bitrates[i-1])
                        num_slots = self.choose_slots_num(distance, demand.bitrates[i])

                        if num_slots != num_slots_prev:
                            self._release_slots(path_idx, demand_idx)
                            out = self._allocate_slots(num_slots, path_idx, demand_idx)

                        if out == True:
                            break

                if out == False:
                    self.blocked += 1
                
            print(f"Demands: {len(self.demands)}")
            print(f"Blocked Count: {self.blocked}")
            print(f"Blocked Ratio: {self.blocked/len(self.demands)}")
        print("Final results:\n")
        print(f"Blocked requests: {self.blocked}")
        print(f"Blocked ratio: {self.blocked/len(self.demands)}")
        print(f"Allocated Slots: {np.count_nonzero(self.slots)}")
        print(f"Allocated Slots: {np.count_nonzero(self.slots)/(320*36)*100}")
                

    def _allocate_slots(self, num_slots: int, path_idx: np.array, demand_idx: int) -> bool:
        """Allocate slots"""
        slots = np.where(self.slots[path_idx] > 0, 1, 0)
        slots = np.bitwise_and.reduce(slots.astype(int), axis=0)
        idx = np.where(np.convolve(slots, np.ones(num_slots), mode='valid') == 0)[0]

        if idx.size == 0:
            return False
        else:
            start_idx = idx[0]
            self.slots[path_idx, start_idx:start_idx + num_slots] = demand_idx
            return True

    def _release_slots(self, path_idx: np.array, demand_idx: int):
        self.slots[path_idx] = np.where(self.slots[path_idx] == demand_idx, 0, self.slots[path_idx])
        
if __name__ == "__main__":
    demands = load_demands("POL12/demands_6")
    paths = load_paths("POL12/pol12.pat")
    xd = FirstFit(demands=demands, paths=paths, distances=distances)
    xd.find_path()
    