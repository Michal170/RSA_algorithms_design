import numpy as np


# TODO
# Probably class not needed, would be good to have script instead class. We can discuss about it
class Verification:
    def __init__(self, file, dataset, slot) -> None:
        self.filename = file
        self.content = self.read_algorith_result()
        self.dataset = dataset
        self.slot = slot

    def read_algorith_result(self):
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
        print(
            f"  {round(counts/(shape*self.slot) * 100, 2)}%          |            {round((((probe-capacity)/probe)*100),2)}%"
        )
        occupancy = round(counts / (shape * self.slot), 5)
        block = round(((probe - capacity) / probe), 5)
        return [occupancy, block]
