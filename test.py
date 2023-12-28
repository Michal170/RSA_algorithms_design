import numpy as np


# TODO
# Probably class not needed, would be good to have script instead class. We can discuss about it
class Verification:
    def __init__(self, file) -> None:
        self.filename = file
        self.content = self.read_algorith_result()

    def read_algorith_result(self):
        content = np.genfromtxt(self.filename)
        return content

    def verify_algorithm(self):
        requests = self.content
        unique_requests = np.unique(requests)
        missing_requests = set(range(500)) - set(unique_requests)

        if not missing_requests:
            print("\nObsłużono wszystkie requesty")
        else:
            print(f"\nW pliku brakuje następujących requestów: {missing_requests}")

    def count_slot_occupancy(self):
        requests = np.count_nonzero(self.content.astype(int))
        print(f"\nZajętość slotów wynosi: {round(requests/(36*320) * 100, 2)}%")
