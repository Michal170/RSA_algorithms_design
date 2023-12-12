from unittest import case
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

def choose_num_slots(distance: int, bitrate: int) -> int:
    slots = 0
    if bitrate <= 200:
        slots = 6
    elif 200 < bitrate and bitrate <= 400:
        if distance <= 800:
            slots = 6
        else:
            slots = 9
    elif 400 < bitrate and bitrate <= 600:
        if distance <= 1600:
            slots = 9
    elif 600 < bitrate and bitrate <= 800:
        if distance <= 200:
            slots = 9

    return slots


if __name__ == "__main__":
    #X = PathStore.load_data("POL12/pol12.pat")
    #np.savetxt("szczecin-kolobrzeg.csv", X[0],  fmt='%d')
    #dd = [paths_names[x] for x in range(36) if X[0,2,x]==1]
    #print(dd)

    print(choose_num_slots(distance=1000, bitrate=340))
        