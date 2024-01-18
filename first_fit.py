import csv
import numpy as np
from helpers.import_data import load_paths, load_demands

# from demand import Demand
from helpers.mappings import path_names, path_index
from helpers.distances import distances
from base import Base
from test import Verification
from helpers.distances import import_distances
import math


class OpticalNetwork(Base):
    def __init__(self, node, data, dataset) -> None:
        super().__init__()
        self.node = node
        self.dataset = dataset
        self.path_index = path_index
        self.distances = distances
        self.path_matrix = load_paths(f"./{dataset}/{dataset}.pat")
        # self.path_matrix = load_paths(f"./US26/us26.pat")
        # self.path_matrix = load_paths("./POL12/pol12.pat")
        self.requests_matrix = load_demands(f"./{dataset}/demands_{data}")
        # self.requests_matrix = load_demands(f"./POL12/demands_{data}")
        self.distances_matrix = import_distances(f"{dataset}/{dataset}.net")
        # self.distances_matrix = import_distances("POL12/pol12.net")
        self.slot_matrix = np.zeros((320, np.shape(self.path_matrix)[2]), dtype=int)
        self.blocks = []
        self.iteration = 1
        self.slots_to_reserve = 0
        self.slots_to_reserve_worst_fit = []
        self.path_nodes = []
        self.distance = 0

    def allocate_first_fit_part(self):
        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            self.number_of_slots = self.choose_slots_num(self.distance, request[3])
            number_index = self.calcute_path_matrix_number()
            self.find_path_and_slots(number_index)
            self.iteration = self.iteration + 1

        np.savetxt("reserve_ff.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block_ff.txt", self.blocks, fmt="%d", delimiter="\t")
        result = Verification("reserve_ff.txt", self.dataset)
        result.verify_algorithm()
        # result.count_slot_occupancy()
        return self.slot_matrix

    def allocate_worst_fit_part(self):
        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            self.number_of_slots = self.choose_slots_num(self.distance, request[3])
            number_index = self.calcute_path_matrix_number()
            self.find_path_and_slots_worst_fit(number_index)
            self.iteration = self.iteration + 1

        np.savetxt("reserve_wf.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block_wf.txt", self.blocks, fmt="%d", delimiter="\t")
        result = Verification("reserve_wf.txt", self.dataset)
        result.verify_algorithm()
        # result.count_slot_occupancy()
        return self.slot_matrix

    def allocate_worst_fit_part_next(self):
        index = 4

        for bitrate_value in range(4, np.shape(self.requests_matrix)[1]):
            count = 0
            for request in self.requests_matrix:
                slots = Base.choose_slots_num(800, request[bitrate_value])
                previous_slots = Base.choose_slots_num(800, request[bitrate_value - 1])
                if slots != previous_slots:
                    self.number_of_slots = slots
                    self._release_slots(count)
                    self.source = request[0]
                    self.destination = request[1]
                    self.iteration = count
                    path = self.calcute_path_matrix_number()
                    self.find_path_and_slots_worst_fit(path)
                count += 1

            index += 1
        np.savetxt("reserve_wf_second.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block_wf_second.txt", self.blocks, fmt="%d", delimiter="\t")
        result = Verification("reserve_wf_second.txt", self.dataset)
        result.verify_algorithm()
        # result.count_slot_occupancy()
        return self.slot_matrix

    def allocate_first_fit_part_next(self):
        index = 4

        for bitrate_value in range(4, np.shape(self.requests_matrix)[1]):
            count = 0
            for request in self.requests_matrix:
                slots = Base.choose_slots_num(800, request[bitrate_value])
                previous_slots = Base.choose_slots_num(800, request[bitrate_value - 1])
                if slots != previous_slots:
                    self.number_of_slots = slots
                    self._release_slots(count)
                    self.source = request[0]
                    self.destination = request[1]
                    self.iteration = count
                    path = self.calcute_path_matrix_number()
                    self.find_path_and_slots(path)
                count += 1

            index += 1
            np.savetxt(
                "reserve_ff_second.txt",
                self.slot_matrix,
                fmt="%d",
                delimiter="\t",
            )
            np.savetxt("block_ff_second.txt", self.blocks, fmt="%d", delimiter="\t")
        result_best = Verification("reserve_ff_second.txt", self.dataset)

        # result_best.count_slot_occupancy()
        result_best.verify_algorithm()

    def _release_slots(self, slots):
        index = np.where(self.slot_matrix == slots)
        for idx in range(len(index[0])):
            self.slot_matrix[index[0][idx]][index[1][idx]] = 0

    def calcute_path_matrix_number(self) -> int:
        """
        Calculate start index in path matrix
        """
        if int(self.source) > int(self.destination):
            path_matrix_number = self.node * int(self.source) + int(self.destination)
        else:
            path_matrix_number = (
                self.node * int(self.source) + int(self.destination) - 1
            )
        return path_matrix_number

    def find_path_and_slots(self, path_matrix_number: int) -> list:
        """
        Get 30 best path and find first with avaible slots. If free slots exists, reservation will be done.
        Otherwise route will be added to blocking table.

        """
        path_list = np.array(self.path_matrix[path_matrix_number])
        distance = 0
        for path in path_list:
            index_list = []
            temp_status = False
            for i in range(len(path)):
                if path[i] == 1:
                    index_list.append(i)
                    distance += self.distances_matrix[i]
            self.distance = distance
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

    def find_path_and_slots_worst_fit(self, path_matrix_number: int) -> list:
        """
        Get 30 best path and find first with avaible slots. If free slots exists, reservation will be done.
        Otherwise route will be added to blocking table.

        """
        path_list = np.array(self.path_matrix[path_matrix_number])
        distance = 0
        for path in path_list:
            index_list = []
            temp_status = False
            for i in range(len(path)):
                if path[i] == 1:
                    index_list.append(i)
                    distance += self.distances_matrix[i]
            self.distance = distance
            if self.check_if_slots_empty_worst_fit(index_list):
                temp_status = True
                break
            else:
                continue
        if temp_status == False:
            self.blocks.append([self.source, self.destination, self.iteration])
        else:
            self.reserve_slots(index_list)
        return index_list

    def check_if_slots_empty_worst_fit(self, demands) -> bool:
        """
        Function will checks whether there are enough free slots
        """
        result = np.all(self.slot_matrix[:, demands] == 0, axis=1)
        available_slots = np.where(result)[0]
        self.available_slots = available_slots

        slots_window = []
        current_list = []

        for i in range(1, len(self.available_slots)):
            if self.available_slots[i] == self.available_slots[i - 1] + 1:
                current_list.append(self.available_slots[i])
            else:
                if (
                    len(current_list) > len(slots_window)
                    and len(current_list) >= self.number_of_slots
                ):
                    slots_window = current_list
                current_list = []

        if len(current_list) > (len(slots_window) and self.number_of_slots):
            slots_window = current_list

        if len(slots_window) >= self.number_of_slots and int(self.number_of_slots) != 0:
            self.slots_to_reserve = slots_window[-self.number_of_slots :]
            return True
        else:
            return False

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

        if len(slots_window) == self.number_of_slots and int(self.number_of_slots) != 0:
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

                else:
                    self.blocks.append([self.source, self.destination])
            self.slot_matrix[self.slots_to_reserve[slot]][index] = self.iteration


if __name__ == "__main__":
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    # print("First fit:")
    # first_fit = OpticalNetwork(node)
    # first_fit.allocate_first_fit_part()
    # first_fit.allocate_first_fit_part_next()

    # print("-----------------------------------------")

    # print("Worst fit part:")
    # worst_fit = OpticalNetwork(node)
    # worst_fit.allocate_worst_fit_part()
    # worst_fit.allocate_worst_fit_part_next()
    print("Zajętość slotu   |   Obsłużone żądania")
    for i in range(10):
        # print(f"----------- Iteracja {i+1} ------------")
        # first_fit = OpticalNetwork(node, i)
        # first_fit.allocate_first_fit_part()
        # first_fit.allocate_first_fit_part_next()

        # worst_fit = OpticalNetwork(node, i)
        # worst_fit.allocate_worst_fit_part()
        # worst_fit.allocate_worst_fit_part_next()

        print(f"------------- demands_{i} -------------")
        first_fit = OpticalNetwork(node_pol, i, dataset_pol)
        first_fit.allocate_first_fit_part()
        first_fit.allocate_first_fit_part_next()
        print(f"\n-------Worst fit-------\n")
        worst_fit = OpticalNetwork(node_pol, i, dataset_pol)
        worst_fit.allocate_worst_fit_part()
        worst_fit.allocate_first_fit_part_next()
        print(f"\n##########################################\n")
