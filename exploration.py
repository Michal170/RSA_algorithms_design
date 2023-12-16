import numpy as np
import os
import matplotlib.pyplot as plt
from helpers.import_data import load_demands
from helpers.distances import distances

if __name__ == "__main__":
    X = load_demands("POL12/demands_1")

    print(X.shape)
    print(distances.shape)