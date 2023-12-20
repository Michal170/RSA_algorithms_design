import csv
import numpy as np
from helpers.import_data import load_paths, load_demands
from demand import Demand
from helpers.mappings import path_names, path_index


class OpticalNetwork:
    def __init__(self, node) -> None:
        self.node = node
        # self.slot_matrix = []
        self.path_index = path_index
        self.path_matrix = load_paths("./POL12/pol12.pat")
        self.requests_matrix = load_demands("./POL12/demands_0")
        self.slot_matrix = np.zeros((320, np.shape(self.path_matrix)[2]), dtype=int)
        self.number_of_slots = 9  # Usunąć hardcodowanie!
        self.blocks = []

    def allocate_requests(self):
        self.path_nodes = []

        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            print("request:", request[0], request[1])
            number_index = self.calcute_path_matrix_number(
                int(request[0]), int(request[1])
            )
            self.find_path_and_slots(number_index)
            # break

        print(self.slot_matrix)
        np.savetxt("reserve.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block.txt", self.blocks, fmt="%d", delimiter="\t")
        return self.slot_matrix

    def calcute_path_matrix_number(self, source: int, destination: int) -> int:
        if source > destination:
            path_matrix_number = self.node * source + destination
        else:
            path_matrix_number = self.node * source + destination - 1
        return path_matrix_number

    def find_path_and_slots(self, path_matrix_number: int) -> list:
        path_list = np.array(self.path_matrix[path_matrix_number])
        for path in path_list:
            index_list = []
            for i in range(len(path)):
                if path[i] == 1:
                    index_list.append(i)
            if self.check_if_slots_empty(index_list):
                break
            else:
                continue
        self.reserve_slots(index_list)
        return index_list

    def check_if_slots_empty(self, demands) -> bool:
        result = np.ones(self.slot_matrix.shape[0], dtype=bool)
        for index in demands:
            result &= self.slot_matrix[:, index] == 0
        available_slots = np.where(result)[0]
        # print(available_slots)
        self.available_slots = available_slots
        if np.any(available_slots):
            return True
        else:
            return False

    def reserve_slots(self, index_list):
        for index in index_list:
            if np.shape(self.available_slots)[0] >= self.number_of_slots:
                for slot in range(self.number_of_slots):
                    self.slot_matrix[self.available_slots[slot]][index] = 1
                self.blocks.append([self.source, self.destination])


if __name__ == "__main__":
    node = 11
    algorithm = OpticalNetwork(node)
    result = algorithm.allocate_requests()
