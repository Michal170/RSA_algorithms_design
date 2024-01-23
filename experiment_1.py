from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt
from best_fit_random import BestRandomAlgorithm
from base import Base


def prepare_exp_best_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []
    result = np.zeros((slot, 2), dtype=int)
    print(result.shape)

    for i in range(1, slot):
        first_fit = OpticalNetwork(node_pol, 0, dataset_pol, i)
        slots_occupancy, slot_unserved = first_fit.allocate_first_fit_part()
        result[i][0] = slots_occupancy * 100
        result[i][1] = slot_unserved * 100

        c, d = first_fit.allocate_first_fit_part_next()
    plt.figure(1)
    plt.plot(
        result[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result[:, 1],
        color="red",
        linestyle="--",
        label="Żądanie nieobsłużone",
        linewidth=0.5,
    )
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xticks(np.arange(0, slot, 20))
    plt.xlim(0, slot)
    plt.ylim(0, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, best fit, zbiór POL12")
    plt.legend()
    plt.savefig("img/best_fit_pol12.png", dpi=150)


def prepare_exp_worst_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []
    result = np.zeros((slot, 2), dtype=int)
    print(result.shape)

    for i in range(1, slot):
        first_fit = OpticalNetwork(node_pol, 0, dataset_pol, i)
        slots_occupancy, slot_unserved = first_fit.allocate_worst_fit_part
        result[i][0] = slots_occupancy * 100
        result[i][1] = slot_unserved * 100

        c, d = first_fit.allocate_first_fit_part_next()
    plt.figure(1)
    plt.plot(
        result[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result[:, 1],
        color="red",
        linestyle="--",
        label="Żądanie nieobsłużone",
        linewidth=0.5,
    )
    plt.xticks(np.arange(1, slot, 20))
    plt.xlim(1, slot)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, worst fit, zbiór POL12")
    plt.legend()
    plt.savefig("worst_fit_pol12.png", dpi=150)
    print(result)


def prepare_exp_random_best_fit_first_alloc():
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
        color="red",
        linestyle="--",
        label="Żądanie nieobsłużone",
        linewidth=0.5,
    )
    plt.xticks(np.arange(1, 1000, 50))
    plt.xlim(1, 1000)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1 dla best fit z losowym wybieranie ścieżki, zbiór POL12")
    plt.legend()
    plt.savefig("best__random_fit_pol12.png", dpi=150)


if __name__ == "__main__":
    wrap = Base()

    @wrap.measure_execution_time(prepare_exp_best_fit_first_alloc())
    def main():
        prepare_exp_best_fit_first_alloc()
        # prepare_exp_worst_fit_first_alloc()

    @wrap.measure_execution_time(prepare_exp_best_fit_first_alloc())
    def main_2():
        prepare_exp_worst_fit_first_alloc()

    main_2()
