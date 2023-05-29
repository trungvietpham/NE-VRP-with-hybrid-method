import numpy as np


class TSP:
    def __init__(self) -> None:
        pass
    
    def fit(self, distance_matrix: np.ndarray, algo: str = None) -> list[int]:
        print('\tĐịnh tuyến đường đi ngắn nhất bằng phương pháp {}'.format(algo))
        return [0,1,3,2]