import numpy as np

from helpers.path_names import paths_names

class PathStore(object):
    def __init__(self):
        pass
    
    @staticmethod
    def load_data(path: str) -> np.array:
        X = np.loadtxt(path, dtype=int)    
        length = int(len(X)/30)
        X = X.reshape((length, 30, 36))
        return np.array(X)

if __name__ == "__main__":
    X = PathStore.load_data("POL12/pol12.pat")
    np.savetxt("szczecin-kolobrzeg.csv", X[0],  fmt='%d')
    dd = [paths_names[x] for x in range(36) if X[0,2,x]==1]
    print(dd)
        