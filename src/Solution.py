import sys
sys.path.append("")
from Phase1 import Phase1
from Phase2 import Phase2
from PrepareData import PrepareData

class Solution:
    def __init__(self) -> None:
        return 
    
    def find_solution(self):
        all_data = PrepareData('vehicle_fname', 'node_fname', 'correlation_fname', 'order_fname').execute()
        Phase1(None, None, None).execute(None, None)
        Phase2(None, None, None).execute(None, None)
        # Visualize()