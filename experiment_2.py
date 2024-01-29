from first_fit import OpticalNetwork
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import timeit
from last_fit import LastFit
from best_fit import BestFit
from tabulate import tabulate
from first_fit_random import First_Fit_Random_Path


def expe_2(node, dataset, scope=10, slot=320):
    """Measurement of the time needed to execute each of the 4 algorithms"""

    name_list = [OpticalNetwork, LastFit, BestFit, First_Fit_Random_Path]
    alg_name = ["FirstFit", "LastFit", "BestFit", "FFRandomAlgorithm"]
    headers = [
        "Dataset",
        "Occupied slots[%]",
        "Processed requests[%]",
        "Execution time[s]",
    ]
    for j in range(len(name_list)):
        print(f"Eksperyment nr.2, Algorytm {alg_name[j]}")
        data = []
        file_name = alg_name[j]
        for i in range(scope):
            print("demnd_", i)
            a = np.zeros(10)
            b = np.zeros(10)
            time_exec = []
            for k in range(10):
                start_time = time.time()
                row = [f"demands_{i}"]

                alg = name_list[j]
                func = alg(node, i, dataset, slot)
                func.allocate_part()
                a_k, b_k = func.allocate_part_next()
                a[k] = a_k
                b[k] = b_k
                end_time = time.time()

                execution_time = end_time - start_time
                time_exec.append(execution_time)
            average_a = np.mean(a)
            average_b = np.mean(b)
            average_time_exec = np.mean(time_exec)
            row.extend([average_a, average_b, round(average_time_exec, 2)])

            data.append(row)

        table = tabulate(data, headers, tablefmt="grid")
        os.makedirs("tables", exist_ok=True)
        output_file_path = os.path.join("tables", f"exp_2_{file_name}_{dataset}.txt")
        table_lt = tabulate(data, headers, tablefmt="latex")
        with open(output_file_path, "w") as file:
            file.write(table + "\n\n" + table_lt)


if __name__ == "__main__":
    """Eksperyment nr.2
    Należy uruchomić ten plik, wyniki będą dostępne w katalogu tables/exp_2_*"""
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    expe_2(node_us, dataset_us, 10, slot)
