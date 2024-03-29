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


def expe_3(node, dataset, scope=10, fill=0):
    """Measurement of the time needed to execute each of the 4 algorithms"""
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    result = []

    result = np.zeros((slot, 2), dtype=int)
    name_list = [OpticalNetwork, LastFit, BestFit, First_Fit_Random_Path]
    alg_name = ["FirstFit", "LastFit", "BestFit", "FFRandomAlgorithm"]
    headers = [
        "Dataset",
        "Processed requests(fill=0%)[%]",
        "Processed requests(fill=5%)[%]",
        "Processed requests(fill=15%)[%]",
        "Processed requests(fill=25%)[%]",
    ]
    fill = [0.0, 0.05, 0.15, 0.25]
    for j in range(4):
        print(f"Eksperyment nr.3, Algorytm{alg_name[j]}")
        data = []
        file_name = alg_name[j]
        for i in range(scope):
            print("demand_", i)
            time_record = []
            data_temp = []
            for k in range(len(fill)):
                a = np.zeros(10)
                b = np.zeros(10)
                time_exec = []
                for h in range(10):
                    start_time = time.time()
                    row = [f"{dataset}/demands_{i}"]
                    row_time = [f" "]

                    alg = name_list[j]
                    func = alg(node, i, dataset, slot, fill[k])
                    func.allocate_part()
                    a_k, b_k = func.allocate_part_next()
                    a[h] = a_k
                    b[h] = b_k
                    end_time = time.time()

                    execution_time = end_time - start_time
                    time_exec.append(execution_time)
                average_a = np.mean(a)
                average_b = np.mean(b)
                average_time_exec = np.mean(time_exec)
                data_temp.append(round(average_b, 2))

                time_record.append(f"{round(average_time_exec,2)}s")
            row.extend([(data_temp[0]), data_temp[1], data_temp[2], data_temp[3]])
            row_time.extend(
                [(time_record[0]), time_record[1], time_record[2], time_record[3]]
            )

            data.append(row)
            data.append(row_time)

        table = tabulate(data, headers, tablefmt="grid")
        os.makedirs("tables", exist_ok=True)
        output_file_path = os.path.join("tables", f"exp_3_{file_name}_{dataset}.txt")
        table_lt = tabulate(data, headers, tablefmt="latex")
        with open(output_file_path, "w") as file:
            file.write(table + "\n\n" + table_lt)


if __name__ == "__main__":
    """Eksperyment nr.3
    Należy uruchomić ten plik, wyniki będą dostępne w katalogu tables/exp_3_*"""
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    expe_3(node_pol, dataset_pol, 10)
