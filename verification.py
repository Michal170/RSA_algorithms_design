import numpy as np


# TODO
# Probably class not needed, would be good to have script instead class. We can discuss about it
class Verification:
    def __init__(self, file, dataset, slot) -> None:
        self.filename = file
        self.content = self.read_algorithm_result()
        self.dataset = dataset
        self.slot = slot

    def read_algorithm_result(self):
        content = np.genfromtxt(self.filename)
        return content

    def verify_algorithm(self):
        if self.dataset == "us26":
            probe = 1000
            shape = 84
        else:
            probe = 500
            shape = 36
        requests = self.content
        unique_requests = np.unique(requests)
        missing_requests = set(range(probe)) - set(unique_requests)

        capacity = len(missing_requests)
        counts = np.count_nonzero(self.content.astype(int))
        occupancy = round(counts / (shape * self.slot), 5) * 100
        block = round(((probe - capacity) / probe), 5) * 100
        print(
            f"Zajętość:{round(occupancy,2)}%          |            Obsłużono {round(block,2)}% żądań "
        )
        return [occupancy, block]
