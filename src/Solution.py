import sys
sys.path.append("")
from Phase1 import Phase1
from Phase2 import Phase2
from PrepareData import PrepareData

class Solution:
    def __init__(self) -> None:
        return 
    
    def find_solution(self):
        all_data = PrepareData(r'data\vehicles.csv', r'data\node.csv', r'data\correlations.csv', r'data\order.csv').execute()
        encode = []
        decode = encode[::-1]
        for i in range(len(encode) - 1):
            Phase1(all_data[1], all_data[2], all_data[3]).execute(all_data[0][encode[i]], all_data[0][encode[i+1]])
            Phase2(None, None, None).execute(None, None)
        # Visualize()