import csv
import numpy as np
from helpers.import_data import load_paths, load_demands
from demand import Demand
from helpers.mappings import path_names, path_index
from helpers.distances import distances
from base import Base
from test import Verification
import math


class OpticalNetwork(Base):
    def __init__(self, node) -> None:
        self.node = node
        self.path_index = path_index
        self.distances = distances
        self.path_matrix = load_paths("./POL12/pol12.pat")
        self.requests_matrix = load_demands("./POL12/demands_0")
        self.slot_matrix = np.zeros((320, np.shape(self.path_matrix)[2]), dtype=int)
        self.blocks = []
        self.iteration = 1
        self.slots_to_reserve = 0
        self.path_nodes = []

    def allocate_first_fit_part(self):
        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            self.number_of_slots = Base.choose_slots_num(800, request[3])
            number_index = self.calcute_path_matrix_number(
                int(request[0]), int(request[1])
            )
            self.find_path_and_slots(number_index)
            self.iteration = self.iteration + 1
            # break

        np.savetxt("reserve.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block.txt", self.blocks, fmt="%d", delimiter="\t")
        return self.slot_matrix

    def allocate_best_fit_part(self):
        index = 3
        count = 0
        for bitrate in range(3, len(self.requests_matrix)):
            deman = 1
            for request in self.requests_matrix:
                if not math.isnan(request[bitrate - 1]):
                    slots = Base.choose_slots_num(800, request[bitrate])
                    previous_slots = Base.choose_slots_num(800, request[bitrate - 1])
                    if slots != previous_slots:
                        print(
                            "Różnica slotów",
                            #     "nr.bitratu:",
                            #     index,
                            previous_slots,
                            slots,
                            "nr.żądania:",
                            deman - 1,
                            "iteracja",
                            count,
                        )
                        count += 1
                    deman += 1
                    # break
            if bitrate == np.shape(self.requests_matrix)[1] - 1:
                break
            index += 1
        print(f"Ilość zmian:{count}")
        print(f"Ilość iteracji:{index}")

    def calcute_path_matrix_number(self, source: int, destination: int) -> int:
        """
        Calculate start index in path matrix
        """
        if source > destination:
            path_matrix_number = self.node * source + destination
        else:
            path_matrix_number = self.node * source + destination - 1
        return path_matrix_number

    def find_path_and_slots(self, path_matrix_number: int) -> list:
        """
        Get 30 best path and find first with avaible slots. If free slots exists, reservation will be done.
        Otherwise route will be added to blocking table.

        """
        path_list = np.array(self.path_matrix[path_matrix_number])
        for path in path_list:
            index_list = []
            temp_status = False
            for i in range(len(path)):
                if path[i] == 1:
                    index_list.append(i)
            if self.check_if_slots_empty(index_list):
                temp_status = True
                break
            else:
                continue
        if temp_status == False:
            self.blocks.append([self.source, self.destination, self.iteration])
        else:
            self.reserve_slots(index_list)
        return index_list

    def check_if_slots_empty(self, demands) -> bool:
        """
        Function will checks whether there are enough free slots
        """
        result = np.ones(self.slot_matrix.shape[0], dtype=bool)
        for index in demands:
            result &= self.slot_matrix[:, index] == 0
        available_slots = np.where(result)[0]
        self.available_slots = available_slots

        slots_window = []

        for i in range(0, len(self.available_slots)):
            if self.available_slots[i] == self.available_slots[i - 1] + 1:
                slots_window.append(self.available_slots[i])
            else:
                slots_window = [self.available_slots[i]]

            if len(slots_window) == self.number_of_slots:
                break

        if len(slots_window) == self.number_of_slots:
            self.slots_to_reserve = slots_window

            return True
        else:
            return False

    def reserve_slots(self, index_list):
        """
        Function makes a reservation
        """
        for index in index_list:
            for slot in range(self.number_of_slots):
                if np.shape(self.slots_to_reserve)[0] >= self.number_of_slots:
                    for slot in range(self.number_of_slots):
                        self.slot_matrix[self.slots_to_reserve[slot]][
                            index
                        ] = self.iteration
                        # print(self.iteration)

                else:
                    self.blocks.append([self.source, self.destination])
            self.slot_matrix[self.slots_to_reserve[slot]][index] = self.iteration


if __name__ == "__main__":
    node = 11
    algorithm = OpticalNetwork(node)
    algorithm.allocate_first_fit_part()
    algorithm.allocate_best_fit_part()

    result = Verification()
    result.verify_algorithm()
    result.count_slot_occupancy()
