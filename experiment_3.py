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


def expe_3(node, dataset, scope=10, fill=0):
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
        "Processed requests(fill=0%)[%]",
        "Processed requests(fill=5%)[%]",
        "Processed requests(fill=15%)[%]",
        "Processed requests(fill=25%)[%]",
    ]
    fill = [0.0, 0.05, 0.15, 0.25]
    for j in range(4):
        data = []
        file_name = alg_name[j]
        for i in range(scope):
            time_record = []
            b = []
            for k in range(len(fill)):
                start_time = time.time()
                # print(k, fill[k])
                row = [f"{dataset}/demands_{i}"]
                row_time = [f" "]

                alg = name_list[j]
                func = alg(node, i, dataset, slot, fill[k])
                func.allocate_part()
                a, b_ = func.allocate_part_next()
                end_time = time.time()

                execution_time = end_time - start_time
                b.append(round(b_, 2))
                time_record.append(f"{round(execution_time,2)}s")
            # print("lista:", b)
            row.extend([(b[0]), b[1], b[2], b[3]])
            row_time.extend(
                [(time_record[0]), time_record[1], time_record[2], time_record[3]]
            )

            data.append(row)
            data.append(row_time)

        table = tabulate(data, headers, tablefmt="grid")
        os.makedirs("tables", exist_ok=True)
        # file_name = alg_name[alg]
        output_file_path = os.path.join("tables", f"exp_3_{file_name}_{dataset}.txt")
        table_lt = tabulate(data, headers, tablefmt="latex")
        with open(output_file_path, "w") as file:
            file.write(table + "\n\n" + table_lt)


if __name__ == "__main__":
    node_us = 25
    node_pol = 11
    dataset_us = "us26"
    dataset_pol = "pol12"
    slot = 320
    expe_3(node_us, dataset_us, 10)
