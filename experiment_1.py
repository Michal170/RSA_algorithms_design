from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt


def prepare_exp_best_best():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []
    result = np.zeros((slot, 2), dtype=int)
    print(result.shape)
    print("Zajętość slotów   |   Obsłużone żądania")
    for i in range(1, slot):
        print(f"------------- demands_{i} -------------")
        first_fit = OpticalNetwork(node_pol, 0, dataset_pol, i)
        slots_occupancy, slot_unserved = first_fit.allocate_first_fit_part()
        print(slots_occupancy, "|", slot_unserved)
        result[i][0] = slots_occupancy * 100
        result[i][1] = slot_unserved * 100

        c, d = first_fit.allocate_first_fit_part_next()
    # fig, ax = plt.subplots()
    plt.plot(result[:, 0], color="blue", label="zajetosc", linewidth=2)
    plt.plot(
        result[:, 1],
        color="red",
        linestyle="--",
        label="zablokowane sloty",
        linewidth=1,
    )
    plt.legend()
    plt.savefig("best_fit.png", dpi=3000)


if __name__ == "__main__":
    prepare_exp_best_best()
