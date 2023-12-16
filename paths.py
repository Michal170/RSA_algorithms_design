from unittest import case
import numpy as np

from helpers.mappings import path_names
from helpers.distances import distances
from helpers.import_data import load_demands, load_paths, load_demands


if __name__ == "__main__":
    paths = load_paths("POL12/pol12.pat")
    np.savetxt("szczecin-kolobrzeg.csv", paths[0],  fmt='%d')
    dd = [distances[x] for x in range(36) if paths[0,2,x]==1]
    names = [path_names[x] for x in range(36) if paths[0,2,x]==1]

    for i in range(len(dd)):
        print(f"Ścieżka {names[i]} -> Distance {dd[i]} km")

    # Jakiś sposób na wybór ścieżek należących do danej pary węzłów
    demands = load_demands("POL12/demands_0")
    print(paths.shape)
