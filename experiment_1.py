from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt
from best_fit_random import BestRandomAlgorithm
from base import Base


def prepare_exp_first_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []
    result = np.zeros((slot, 2), dtype=int)
    print(result.shape)

    for i in range(1, slot):
        first_fit = OpticalNetwork(node_us, 0, dataset_us, i)
        slots_occupancy, slot_unserved = first_fit.allocate_first_fit_part()
        result[i][0] = slots_occupancy * 100
        result[i][1] = slot_unserved * 100

        # c, d = first_fit.allocate_first_fit_part_next()
    plt.figure(1)
    plt.plot(
        result[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result[:, 1],
        color="green",
        linestyle="--",
        label="Żądania obsłużone",
        linewidth=0.5,
    )
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xticks(np.arange(0, slot, 20))
    plt.xlim(0, slot)
    plt.ylim(0, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, First Fit, zbiór US26/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_first_fit_us26.png", dpi=150)


def prepare_exp_last_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 500
    result_wf = []
    result_wf = np.zeros((slot, 2), dtype=int)
    print(result_wf.shape)

    for i in range(1, slot):
        first_fit = OpticalNetwork(node_us, 0, dataset_us, i)
        slots_occupancy, slot_unserved = first_fit.allocate_last_fit_part()
        result_wf[i][0] = slots_occupancy * 100
        result_wf[i][1] = slot_unserved * 100

    plt.figure(1)
    plt.plot(
        result_wf[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result_wf[:, 1],
        color="green",
        linestyle="--",
        label="Żądania obsłużone",
        linewidth=0.5,
    )
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xticks(np.arange(0, slot, 20))
    plt.xlim(1, slot)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, Last fit, zbiór US26/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_last_fit_us26.png", dpi=150)
    print(result_wf)


def prepare_exp_random_first_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 201
    result = []
    result = np.zeros((slot, 2), dtype=int)
    # print(result.shape)

    for i in range(200, slot):
        print("Iteracja eksperymentu:", i)
        first_fit = BestRandomAlgorithm(i)
        slots_occupancy, slot_unserved = first_fit.best_random_algorithm()
        result[i][0] = slots_occupancy * 100
        result[i][1] = slot_unserved * 100

    plt.figure(1)
    plt.plot(
        result[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result[:, 1],
        color="green",
        linestyle="--",
        label="Żądania obsłużone",
        linewidth=0.5,
    )
    plt.xticks(np.arange(1, 1000, 50))
    plt.xlim(1, 1000)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1 dla First Fit z losowym wybieranie ścieżki, zbiór us26")
    plt.legend()
    plt.savefig("img/exp_1_first_random_fit_us26.png", dpi=150)


if __name__ == "__main__":
    # prepare_exp_first_fit_first_alloc()
    prepare_exp_last_fit_first_alloc()
