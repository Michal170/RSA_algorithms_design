import csv
import numpy as np
from helpers.import_data import load_paths, load_demands
from helpers.mappings import path_names, path_index
from helpers.distances import distances
from base import Base
from verification import Verification
from helpers.distances import import_distances
from verification import Verification
import math
import random


class BestRandomAlgorithm(Base):
    def __init__(self, node_num: int = 12) -> None:
        super().__init__(node_num)
        self.node = 11
        self.slot = 950
        dataset = "pol12"
        self.block = []
        data = 0
        self.path_matrix = load_paths(f"./pol12/pol12.pat")
        # print(self.path_matrix.shape)
        self.requests_matrix = load_demands(f"./{dataset}/demands_{data}")
        self.distances_matrix = import_distances(f"{dataset}/{dataset}.net")
        self.iteration = 1
        self.blocks = []
        self.blocked_request = []

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

        return np.array(self.path_matrix[path_matrix_number])

    def best_random_algorithm(self):
        self.slot_matrix = np.zeros(
            (self.slot, np.shape(self.path_matrix)[2]), dtype=int
        )
        for request in self.requests_matrix:
            self.source = request[0]
            self.destination = request[1]
            self.bitrate = request[3]
            self.path_matrix_data = self.calcute_path_matrix_number()
            self.find_slot()
            self.iteration = self.iteration + 1

            np.savetxt("reserve_rand.txt", self.slot_matrix, fmt="%d", delimiter="\t")
        np.savetxt("block_rand.txt", self.blocked_request, fmt="%d", delimiter="\t")
        result = Verification("reserve_rand.txt", "pol12", self.slot)
        result.read_algorithm_result()
        # result.verify_algorithm()
        occupancy, block = result.verify_algorithm()
        return occupancy, block
        # break

    def draw_path(self):
        path_index = np.random.randint(0, 29)
        # print("wylosowany index:", path_index)
        return path_index

    def find_slot(self):
        flag = False
        index_draw_list = []
        index_list = []
        while flag == False:
            index = self.draw_path()
            if index in index_draw_list:
                continue
            if index not in index_draw_list:
                index_draw_list.append(index)
            if len(index_draw_list) >= 29:
                self.blocked_request.append(self.iteration)
                # print(self.blocks)
                # print(f"BREAK{self.iteration}")
                flag = True
                break

            distance = 0
            for i in range(len(self.path_matrix_data[index])):
                if self.path_matrix_data[index][i] == 1:
                    index_list.append(i)
                    distance += self.distances_matrix[i]
            self.index_list = index_list
            self.distance = distance
            self.number_of_slots = self.choose_slots_num(self.distance, self.bitrate)
            result = np.ones(self.slot_matrix.shape[0], dtype=bool)
            for index in index_list:
                result &= self.slot_matrix[:, index] == 0
            self.available_slots = np.where(result)[0]
            flag = self.check_if_slot_empty()
            # print("flaga:", flag, self.slots_to_reserve)
            # print(self.slots_to_reserve)
            result = self.reserve_slots(index_list)
            # flag = True
            if flag == True:
                index_list = []
                index_draw_list = []

    def check_if_slot_empty(self):
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
            # print("Sloty do rezerwacji:", slots_window)
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
                        a = self.slot_matrix[self.slots_to_reserve[slot]][index]
                        # print(a)
                        self.slot_matrix[self.slots_to_reserve[slot]][
                            index
                        ] = self.iteration

                        # print(f"dodano { self.iteration}")

                else:
                    self.blocks.append([self.source, self.destination])
        return True
        # self.slot_matrix[self.slots_to_reserve[slot]][index] = self.iteration


if __name__ == "__main__":
    alg = BestRandomAlgorithm()
    alg.best_random_algorithm()
