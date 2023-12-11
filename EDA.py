import numpy as np
import os
import matplotlib.pyplot as plt


def import_data(data_dir: str) -> np.array:
    data = []
    dirs = os.listdir(data_dir)
    for i in dirs:
        if  os.path.isdir(os.path.join(data_dir, i)):
            d_part = []
            for d in os.listdir(os.path.join(data_dir, i)):
                d_part.append(np.genfromtxt(os.path.join(data_dir, i, d)))
            data.append(d_part)
    return np.array(data)


if __name__ == "__main__":
    X = import_data("POL12")
    print(X[0,:,3])

    #plt.plot(X[0,:,3])
    #plt.savefig("xd.png")