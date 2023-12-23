import numpy as np


class Verification:
    def __init__(self) -> None:
        self.content = self.read_algorith_result()

    def read_algorith_result(self):
        with open("reserve.txt", "r") as slots_reservation:
            content = slots_reservation.read()
        return content

    def verify_algorithm(self):
        requests = self.content.split()
        unique_requests = set(map(int, requests))
        missing_requests = set(range(500)) - unique_requests

        if not missing_requests:
            print("Obsłużono wszystkie requesty")
        else:
            print(f"W pliku brakuje następujących requestów: {missing_requests}")

    def count_slot_occupancy(self):
        requests = self.content.split()
        suma = sum(1 for request in map(int, requests))
        non_zero_count = sum(1 for request in map(int, requests) if request != 0)
        result = round((non_zero_count / suma), 2)
        print(f"Zajętość slotów wynosi:{result}")
