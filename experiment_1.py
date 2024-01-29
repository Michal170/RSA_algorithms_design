from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt
from first_fit_random import First_Fit_Random_Path
from last_fit import LastFit
from best_fit import BestFit
from base import Base
from helpers.time_measure import measure_time


@measure_time
def prepare_exp_first_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 800
    result = []
    result = np.zeros((slot, 2), dtype=int)

    for i in range(1, slot):
        print(f"------ slot:{i}  ------")
        first_fit = OpticalNetwork(node_us, 0, dataset_us, i)
        first_fit.allocate_part()
        slots_occupancy, slot_unserved = first_fit.allocate_part_next()
        result[i][0] = slots_occupancy
        result[i][1] = slot_unserved

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
    plt.xticks(np.arange(0, slot, 50))
    plt.xlim(0, slot)
    plt.ylim(0, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, First Fit, zbiór US26/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_first_fit_us26.png", dpi=150)


@measure_time
def prepare_exp_best_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 800
    result = []
    result = np.zeros((slot, 2), dtype=int)

    for i in range(1, slot):
        print(f"------ slot:{i}  ------")
        first_fit = BestFit(node_pol, 0, dataset_pol, i)
        first_fit.allocate_part()
        slots_occupancy, slot_unserved = first_fit.allocate_part_next()
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
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xticks(np.arange(0, slot, 25))
    plt.xlim(0, slot)
    plt.ylim(0, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, Best Fit, zbiór POL12/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_best_fit_pol12.png", dpi=150)


@measure_time
def prepare_exp_last_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 800
    result_wf = []
    result_wf = np.zeros((slot, 2), dtype=int)

    for i in range(1, slot):
        print(f"------ slot:{i}  ------")
        first_fit = LastFit(node_us, 0, dataset_us, i)
        first_fit.allocate_part()
        slots_occupancy, slot_unserved = first_fit.allocate_part_next()
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
    plt.xticks(np.arange(0, slot, 50))
    plt.xlim(1, slot)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("Eksperyment nr.1, Last fit, zbiór US26/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_last_fit_us26.png", dpi=150)
    print(result_wf)


@measure_time
def prepare_exp_random_first_fit_first_alloc():
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 1100
    result_rand = []
    result_rand = np.zeros((slot, 2), dtype=int)

    for i in range(10, slot):
        print(f"------ slot:{i}  ------")
        first_fit = First_Fit_Random_Path(node_pol, 0, dataset_pol, i)
        slots_occupancy, slot_unserved = first_fit.allocate_part()
        result_rand[i][0] = slots_occupancy * 100
        result_rand[i][1] = slot_unserved * 100

    plt.figure(1)
    plt.plot(
        result_rand[:, 0], color="blue", label="Zajętość dostępnych slotów", linewidth=1
    )
    plt.plot(
        result_rand[:, 1],
        color="green",
        linestyle="--",
        label="Żądania obsłużone",
        linewidth=0.5,
    )
    plt.grid(which="both", linestyle="--", linewidth=0.5)
    plt.xticks(np.arange(0, slot, 100))
    plt.xlim(1, slot)
    plt.ylim(1, 100)
    plt.xlabel("Ilość dostępnych slotów[szt]")
    plt.ylabel("Zajętość [%]")
    plt.title("F-Fit z losowym wybieraniem ścieżki, zbiór pol12/demands_0")
    plt.legend()
    plt.savefig("img/exp_1_first_random_fit_pol12.png", dpi=150)


if __name__ == "__main__":
    """Eksperyment nr.1. Należy uruchomić wybraną opcję, wyniki będą dostępne w katalogu img/"""
    prepare_exp_first_fit_first_alloc()
    prepare_exp_last_fit_first_alloc()
    prepare_exp_best_fit_first_alloc()
    prepare_exp_random_first_fit_first_alloc()
