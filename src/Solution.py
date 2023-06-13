import sys
sys.path.append("")
from Phase1 import Phase1
from Phase2 import Phase2
from PrepareData import PrepareData

class Solution:
    def __init__(self) -> None:
        return 
    
    def find_solution(self):
        print(f"FUNCTION: {__name__}")
        prepare_phase = PrepareData(r'data\vehicles.csv', r'data\node.csv', r'data\correlations_sample.csv', r'data\order_sample.csv')
        all_data = prepare_phase.execute()
        encode = ['GD3', 'GD2', 'GD1']
        decode = encode[::-1]
        main_order_controller = all_data[2].copy() # For encode phase
        support_order_controller = all_data[2].copy() # for decode phase
        for i in range(len(encode) - 1):
            print(f"sender side: {encode[i]} -> {encode[i+1]}")
            main_order_controller = Phase1(all_data[1], main_order_controller, all_data[3], all_data[4]).execute(all_data[0][encode[i]], all_data[0][encode[i+1]], f'scenarios/output_sender_side.{encode[i]}-{encode[i+1]}.json')
            # Phase2(None, None, None).execute(None, None)
        # Visualize()
        
        # Nếu là receiver side thì append depot id vào order current state trước khi chạy phase 1
        support_order_controller = prepare_phase.update_order_state(support_order_controller, by='end')
        for i in range(len(encode)-1):
            print(f"Receiver side: {encode[i]} -> {encode[i+1]}")
            support_order_controller = Phase1(all_data[1], support_order_controller, all_data[3], all_data[4]).execute(all_data[0][encode[i]], all_data[0][encode[i+1]], f'scenarios/output_receiver_side.{encode[i]}-{encode[i+1]}.json')
        
        
