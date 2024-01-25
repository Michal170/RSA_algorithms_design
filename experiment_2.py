from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import timeit
from last_fit import LastFit
from best_fit import BestFit
from tabulate import tabulate
from best_fit_random import BestRandomAlgorithm


def expe_2(node, dataset, scope=10):
    """Measurement of the time needed to execute each of the 4 algorithms"""
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []

    result = np.zeros((slot, 2), dtype=int)
    name_list = [OpticalNetwork, LastFit, BestFit, BestRandomAlgorithm]
    alg_name = ["FirstFit", "LastFit", "BestFit", "FFRandomAlgorithm"]
    # headers = [
    #     "Zbiór",
    #     "First-Fit",
    #     "First-Fit",
    #     "Last-Fit",
    #     "Last-Fit",
    #     "Best-Fit",
    #     "Best-Fit",
    #     "FF rand path",
    #     "FF rand path",
    # ]
    headers = [
        "Dataset",
        "Occupied slots[%]",
        "Processed requests[%]",
        "Execution time[s]",
    ]
    for j in range(3, 4):
        data = []
        file_name = alg_name[j]
        for i in range(scope):
            start_time = time.time()
            row = [f"demands_{i}"]

            alg = name_list[j]
            func = alg(node, i, dataset, slot)
            func.allocate_part()
            a, b = func.allocate_part_next()
            end_time = time.time()

            execution_time = end_time - start_time
            row.extend([(a), (b), round(execution_time, 2)])

            data.append(row)

        table = tabulate(data, headers, tablefmt="grid")
        os.makedirs("tables", exist_ok=True)
        # file_name = alg_name[alg]
        output_file_path = os.path.join("tables", f"exp_2_{file_name}_{dataset}.txt")
        table_lt = tabulate(data, headers, tablefmt="latex")
        with open(output_file_path, "w") as file:
            file.write(table + "\n\n" + table_lt)


if __name__ == "__main__":
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    expe_2(node_us, dataset_us, 10)
