import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_local_search

class TSP:
    def __init__(self) -> None:
        pass
    
    def fit(self, distance_matrix: np.ndarray, algo: str = None) -> list[int]:
        print('\tĐịnh tuyến đường đi ngắn nhất bằng phương pháp {}'.format(algo))
        
        if algo == 'bitmasking':
            route, distance = solve_tsp_local_search(distance_matrix)
        return route