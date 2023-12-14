import csv
import numpy as np
from paths import PathStore
from demands import Edge
from helpers.path_names import paths_names


class OpticalNetwork:
    def __init__(self, node) -> None:
        self.node = node
        self.slot_matrix = []
        # self.slot_matrix = [[0 for _ in range(320)] for _ in range(11)]
        self.path_matrix = PathStore.load_data("POL12/pol12.pat")
        self.requests_matrix = Edge.load_data("./POL12/demands_0")

    def allocate_requests(self):
        self.slot_matrix = [[0 for _ in range(320)] for _ in range(self.node)]
        print("request_matrix:", np.shape(self.requests_matrix))
        print("Path_matrix:", np.shape(self.path_matrix))
        print("slot_matrix:", np.shape(self.slot_matrix))
        for request in self.requests_matrix:
            source = int(request[0])
            destination = int(request[1])
            print("Source", source, "Destination", destination)
            number_index = self.calcute_path_matrix_number(source, destination)
            self.find_path(number_index)
            break
        return self.slot_matrix

    def calcute_path_matrix_number(self, source: int, destination: int) -> int:
        if source > destination:
            path_matrix_number = self.node * source + destination
        else:
            path_matrix_number = self.node * source + destination - 1
        return path_matrix_number

    def find_path(self, path_matrix_number: int):
        for k in self.path_matrix[path_matrix_number]:
            # paths = [paths_names[x] for x in range(36) if k[x] == 1]
            # print(paths)
            for x in range(36):
                if k[x] == 1:
                    print(x)
            print("------", "\n", "Krawędzie w wybranej ścieżce:")
            # print(k)


#     def __init__(self, num_slots):
#         self.num_slots = num_slots
#         self.network_state = {i: set() for i in range(num_slots)}

#     def allocate_requests(self):
#         requests = self.read_data()
#         results = []
#         for request in requests:
#             source, destination, bitrate = request
#             result = self.first_fit_allocation(source, destination, bitrate)
#             results.append(result)
#         return results

#     def first_fit_allocation(self, source, destination, bitrate):
#         required_slots = self.calculate_required_slots(bitrate)

#         for start_slot in range(self.num_slots - required_slots + 1):
#             end_slot = start_slot + required_slots - 1

#             if all(
#                 not self.is_slot_reserved(slot, source, destination)
#                 for slot in range(start_slot, end_slot + 1)
#             ):
#                 self.reserve_slots(source, destination, start_slot, end_slot)
#                 return f"Alokacja z {source} do {destination} z sukcesem: {start_slot}-{end_slot}"

#         return f"Brak dostępnego widma dla zapotrzebowania z {source} do {destination}"

#     def calculate_required_slots(self, bitrate):
#         if bitrate <= 200:
#             slots = 6
#         else:
#             slots = 9
#         return slots

#     def is_slot_reserved(self, slot, source, destination):
#         if source in self.network_state and destination in self.network_state:
#             return (
#                 slot in self.network_state[source]
#                 or slot in self.network_state[destination]
#             )
#         else:
#             self.network_state[source] = set()
#             self.network_state[destination] = set()
#             return False

#     def reserve_slots(self, source, destination, start_slot, end_slot):
#         for slot in range(start_slot, end_slot + 1):
#             self.network_state[source].add(slot)
#             self.network_state[destination].add(slot)

#     def read_data(self):
#         filename = "requests.csv"
#         data = []

#         with open(filename, "r") as csv_file:
#             loaded_data = csv.reader(csv_file)
#             next(loaded_data)
#             for row in loaded_data:
#                 data.append(tuple(map(float, row[1:])))
#         return data


if __name__ == "__main__":
    node = 11
    algorithm = OpticalNetwork(node)
    result = algorithm.allocate_requests()
    # print("SH:", np.shape(result))

# optical_network = OpticalNetwork(num_slots=100)

# results = optical_network.allocate_requests()
# for result in results:
#     print(result)
