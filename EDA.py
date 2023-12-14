import numpy as np
import os
import matplotlib.pyplot as plt
from helpers.import_data import import_data

if __name__ == "__main__":
    X = import_data("POL12/demands_1")
    print(X.shape)

    #plt.plot(X[0,:,3])
    #plt.savefig("xd.png")