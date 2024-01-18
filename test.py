import numpy as np


# TODO
# Probably class not needed, would be good to have script instead class. We can discuss about it
class Verification:
    def __init__(self, file, dataset) -> None:
        self.filename = file
        self.content = self.read_algorith_result()
        self.dataset = dataset

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

        # if not missing_requests:
        #     # print("Obsłużono wszystkie requesty")
        #     pass
        # else:
        #     print(f"W pliku brakuje następujących requestów: {missing_requests}")

        capacity = len(missing_requests)
        counts = np.count_nonzero(self.content.astype(int))
        print(
            f"  {round(counts/(shape*320) * 100, 2)}%          |            {round((((probe-capacity)/probe)*100),2)}%"
            # f"Zajętość slotów wynosi: {round(counts/(36*320) * 100, 2)}% | {((500-capacity)/500)*100}%"
        )

    # def count_slot_occupancy(self):
    #     requests = np.count_nonzero(self.content.astype(int))
    #     print(f"Zajętość slotów wynosi: {round(requests/(36*320) * 100, 2)}%")


# if __name__ == "__main__":
#     # first_fit = Verification("reserve.txt")
#     # first_fit_two = Verification("reserve_ff_next_iteration.txt")
#     # worst_fit_two = Verification("reserve_worst_fit.txt")
#     # print(
#     #     first_fit.count_slot_occupancy(),
#     #     first_fit_two.count_slot_occupancy(),
#     #     worst_fit_two.count_slot_occupancy(),
#     # )

#     content_1 = np.genfromtxt("reserve_ff_next_iteration.txt", dtype=int)
#     content_2 = np.genfromtxt("reserve_worst_fit.txt", dtype=int)

#     unique_values_1, counts_1 = np.unique(content_1, return_counts=True)
#     unique_values_2, counts_2 = np.unique(content_2, return_counts=True)

#     content_1_tuple = tuple(content_1.tolist())
#     content_2_tuple = tuple(content_2.tolist())

#     set_1 = set(zip(unique_values_1, counts_1))
#     set_2 = set(zip(unique_values_2, counts_2))

#     different_counts = set_1.symmetric_difference(set_2)

#     print("Wartości różniące się pod względem liczności:", different_counts)
#     different_counts = set_2.symmetric_difference(set_1)

#     print("Wartości różniące się pod względem liczności:", different_counts)
