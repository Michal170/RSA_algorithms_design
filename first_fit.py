import csv
import numpy as np
from helpers.import_data import load_paths, load_demands
from helpers.mappings import path_names, path_index
from helpers.distances import distances
from base import Base
from verification import Verification
from helpers.distances import import_distances
import math
import os


class OpticalNetwork(Base):
    def __init__(self, node, data, dataset, slot, fill_factor=0) -> None:
        super().__init__()
        self.node = node
        self.slot = slot
        self.dataset = dataset
        self.path_index = path_index
        self.distances = distances
        self.chosen_path_distances = []
        self.path_matrix = load_paths(f"./{dataset}/{dataset}.pat")
        self.requests_matrix = load_demands(f"./{dataset}/demands_{data}")
        self.distances_matrix = import_distances(f"{dataset}/{dataset}.net")
        self.blocks = []
        self.iteration = 1
        self.slots_to_reserve = 0
        self.slots_to_reserve_last_fit = []
        self.path_nodes = []
        self.distance = 0
        self.fill_factor = fill_factor

    def random_fill(self):
        numb_elem_to_fill = int(self.fill_factor * self.slot_matrix.size)

        idx_to_fill = np.random.choice(
            self.slot_matrix.size, numb_elem_to_fill, replace=False
        )

        self.slot_matrix.flat[idx_to_fill] = np.random.randint(
            1, self.slot, numb_elem_to_fill
        )
        os.makedirs("results", exist_ok=True)
        output_file_path = os.path.join("results", f"fill.txt")
        np.savetxt(output_file_path, self.slot_matrix, fmt="%d", delimiter="\t")

    def allocate_part(self):
        self.slot_matrix = []
        self.slot_matrix = np.zeros(
            (self.slot, np.shape(self.path_matrix)[2]), dtype=int
        )
        self.random_fill()
        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            self.bitrate = request[3]
            number_index = self.calcute_path_matrix_number()
            self.find_path_and_slots(number_index)
            self.iteration = self.iteration + 1

        os.makedirs("results", exist_ok=True)
        output_file_path = os.path.join("results", f"reserve_ff.txt")
        np.savetxt(output_file_path, self.slot_matrix, fmt="%d", delimiter="\t")
        output_file_path = os.path.join("results", f"block_ff.txt")
        np.savetxt(output_file_path, self.blocks, fmt="%d", delimiter="\t")
        result = Verification("results/reserve_ff.txt", self.dataset, self.slot)
        occupancy, block = result.verify_algorithm()
        return occupancy, block

    # def allocate_last_fit_part(self):
    #     self.slot_matrix = []
    #     self.slot_matrix = np.zeros(
    #         (self.slot, np.shape(self.path_matrix)[2]), dtype=int
    #     )
    #     for request in self.requests_matrix:
    #         self.source = request[0]
    #         self.destination = request[1]
    #         self.bitrate = request[3]
    #         number_index = self.calcute_path_matrix_number()
    #         self.find_path_and_slots_last_fit(number_index)
    #         self.iteration = self.iteration + 1

    #     os.makedirs("results", exist_ok=True)
    #     output_file_path = os.path.join("results", f"reserve_wf.txt")
    #     np.savetxt(output_file_path, self.slot_matrix, fmt="%d", delimiter="\t")
    #     output_file_path = os.path.join("results", f"block_wf.txt")
    #     np.savetxt(output_file_path, self.blocks, fmt="%d", delimiter="\t")
    #     result = Verification("results/reserve_wf.txt", self.dataset, self.slot)
    #     occupancy, block = result.verify_algorithm()
    #     return occupancy, block

    # def allocate_last_fit_part_next(self):
    #     index = 4

    #     for bitrate_value in range(4, np.shape(self.requests_matrix)[1]):
    #         count = 0
    #         for request in self.requests_matrix:
    #             slots = Base.choose_slots_num(800, request[bitrate_value])
    #             previous_slots = Base.choose_slots_num(800, request[bitrate_value - 1])
    #             if slots != previous_slots:
    #                 self.number_of_slots = slots
    #                 self._release_slots(count)
    #                 self.source = request[0]
    #                 self.destination = request[1]
    #                 self.iteration = count
    #                 path = self.calcute_path_matrix_number()
    #                 self.find_path_and_slots_last_fit(path)
    #             count += 1

    #         index += 1
    #     os.makedirs("results", exist_ok=True)
    #     output_file_path = os.path.join("results", f"reserve_wf_second.txt")
    #     np.savetxt(output_file_path, self.slot_matrix, fmt="%d", delimiter="\t")
    #     output_file_path = os.path.join("results", f"block_wf_second.txt")
    #     np.savetxt(output_file_path, self.blocks, fmt="%d", delimiter="\t")
    #     result = Verification("results/reserve_wf_second.txt", self.dataset, self.slot)
    #     occupancy, block = result.verify_algorithm()
    #     return occupancy, block

    def allocate_part_next(self):
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
        os.makedirs("results", exist_ok=True)
        output_file_path = os.path.join("results", f"reserve_ff_second.txt")
        np.savetxt(output_file_path, self.slot_matrix, fmt="%d", delimiter="\t")
        output_file_path = os.path.join("results", f"block_ff_second.txt")
        result_best = Verification(
            "results/reserve_ff_second.txt", self.dataset, self.slot
        )

        occupancy, block = result_best.verify_algorithm()
        return occupancy, block

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
            self.number_of_slots = self.choose_slots_num(self.distance, self.bitrate)

            if self.check_if_slots_empty(index_list):
                temp_status = True
                break
            else:
                continue
        self.chosen_path_distances.append(distance)
        if temp_status == False:
            self.blocks.append([self.source, self.destination, self.iteration])
        else:
            self.reserve_slots(index_list)
        return index_list

    def find_path_and_slots_last_fit(self, path_matrix_number: int) -> list:
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
            self.number_of_slots = self.choose_slots_num(self.distance, self.bitrate)
            if self.check_if_slots_empty_last_fit(index_list):
                temp_status = True
                break
            else:
                continue
        if temp_status == False:
            self.blocks.append([self.source, self.destination, self.iteration])
        else:
            self.reserve_slots(index_list)
        return index_list

    def check_if_slots_empty_last_fit(self, demands) -> bool:
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
            # print(slots_window)
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
    slot = 320
    first_fit = OpticalNetwork(node_us, 0, dataset_us, slot, fill_factor=0)
    first_fit.allocate_first_fit_part()
    first_fit.allocate_first_fit_part_next()
# last_fit = OpticalNetwork(node_pol, 0, dataset_pol, slot)
# last_fit.allocate_last_fit_part()
# last_fit.allocate_last_fit_part_next()
