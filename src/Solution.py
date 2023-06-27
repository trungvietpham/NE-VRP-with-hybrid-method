import sys
from BaseClass.Node import NodeController
from BaseClass.Order import OrderController

from Visualize import Visualize
sys.path.append("")
from Phase1 import Phase1
from Phase2 import Phase2
from PrepareData import PrepareData

from time import time
import pickle as pkl
class Solution:
    def __init__(self) -> None:
        return 
    
    def check(self, vehicle_controller_hierarchical, province_node_controller, province_code, province_exist_order_list: list[str]):
        if province_code not in province_exist_order_list: 
            # print(f"{province_code} not found order")
            return False
        if province_code not in vehicle_controller_hierarchical: 
            # print(f"{province_code} not found in vehicle list")
            # input('asdfgh')
            return False
        if 'GD1' not in province_node_controller: 
            # print(f"Province {province_code} don't have GD1 point")
            # input('streurhtor')
            return False
        
        if 'GD2' not in province_node_controller:
            # print(f"Province {province_code} don't have GD2 point")
            return False
        return True
    
    def merge_order(self, order_controller_list) -> OrderController:
        res = OrderController()
        for o_c in order_controller_list:
            res.__add__(o_c)
        return res 
    
    def dump(self, data, filename):
        with open(filename, 'wb') as f: 
            pkl.dump(data, f, pkl.HIGHEST_PROTOCOL)
        return 
    
    def load(self, filename):
        with open(filename, 'wb') as f: 
            return pkl.load(f)
    
    def find_solution(self):
        print(f"FUNCTION: {__name__}")
        times = {}
        t1 = time()
        prepare_phase = PrepareData(r'data\vehicles.tsv', r'data\node.tsv', r'data\correlations.tsv', r'data\order.tsv')
        all_data = prepare_phase.execute()
        self.dump({'data': all_data, 'phase': prepare_phase, 'time': times}, 'dump/prepare_phase.pkl')
        
        # data = pkl.load(open('dump/prepare_phase.pkl', 'rb'))
        # all_data, prepare_phase, times = list(data.values())
        main_all_order = prepare_phase.order_hierachical_by_province(all_data[2].copy())
        times['prepare data'] = time() - t1
        
        # main_all_order = all_order_by_province.copy()
        start_node_controller = NodeController()
        for k in all_data[0]:
            start_node_controller.__add__(all_data[0][k]['GD1'])
        # all_data[0][province_code]['GD1'].copy()
        # start_node_controller = prepare_phase.concatenate(a_dict)
        # all_data[1].print()
        # encode = ['GD2', 'GD1']
        # decode = encode[::-1]
        
        main_order_controller = all_data[2].copy() # For encode phase
        support_order_controller = all_data[2].copy() # for decode phase
        
        print(f"sender side: GD2 -> GD1:")
        phase_data = {}
        # print(main_all_order.keys())
        # input('asdiyhage')
        t1 = time()
        for province_code in all_data[0]:
            print(f"Province code: {province_code}")
            if not self.check(all_data[1], all_data[0][province_code], province_code, list(main_all_order.keys())): continue
            
            all_data[4][province_code]
            phase = Phase1(all_data[1][province_code], main_all_order[province_code], all_data[3], all_data[4][province_code].copy())
            # all_data[0][province_code]['GD2'].print()
            main_all_order[province_code], phase_data = phase.execute(all_data[0][province_code]['GD2'].copy(), all_data[0][province_code]['GD1'].copy(), phase_data)
        
        phase.output_to_json(phase_data, 'scenarios/output_sender_side.GD2-GD1.json')
            # main_order_controller = Phase1(all_data[1], main_order_controller, all_data[3], all_data[4].copy()).execute(all_data[0][encode[i]].copy(), all_data[0][encode[i+1]].copy(), f'scenarios/output_sender_side.{encode[i]}-{encode[i+1]}.json')
        times['phase 1'] = time() - t1
        self.dump({'phase 1': main_all_order, 'time': times}, 'dump/phase1.pkl')
        
        t1 = time()
        # Nếu là receiver side thì append depot id vào order current state trước khi chạy phase 1
        support_order_controller = prepare_phase.update_order_state(support_order_controller, by='end')
        support_all_order = prepare_phase.order_hierachical_by_province(support_order_controller, sender_flag=False)
        print(f"Receiver side: GD1 -> GD2")
        # del phase_data
        phase_data = {}
        for province_code in all_data[0]:
            print(f"Province code: {province_code}")
            if not self.check(all_data[1], all_data[0][province_code], province_code, list(support_all_order.keys())): continue
            
            phase = Phase1(all_data[1][province_code], support_all_order[province_code], all_data[3], all_data[4][province_code].copy())
            support_all_order[province_code], phase_data = phase.execute(all_data[0][province_code]['GD2'].copy(), all_data[0][province_code]['GD1'].copy(), phase_data, reverse=True)
        phase.output_to_json(phase_data, 'scenarios/output_receiver_side.GD2-GD1.json')
        times['phase 3'] = time() - t1
        self.dump({'phase 3': support_all_order, 'time': times}, 'dump/phase3.pkl')
        
        t1 = time()
        main_order_controller = self.merge_order(list(main_all_order.values()))
        support_order_controller = self.merge_order(list(support_all_order.values()))
        # Phase 2:
        vehicle_controller = prepare_phase.concatenate(all_data[1])
        node_contain_vehicle = prepare_phase.concatenate(all_data[4])
        main_order_controller = Phase2(vehicle_controller, main_order_controller, support_order_controller, all_data[3], node_contain_vehicle).execute(start_node_controller, start_node_controller, f'scenarios/output_sender_receiver.GD1-GD1.json')
        times['phase 2'] = time() - t1
        self.dump({'phase 2': main_order_controller, 'time': times}, 'dump/phase2.pkl')
        
        visualize = Visualize(all_data[0], main_order_controller, support_order_controller)
        order_path = visualize.get_order_route()
        vehicle_path = visualize.get_vehicle_route()
        # print(order_path)
        visualize.output_to_file(order_path, 'scenarios/order.json')
        visualize.output_to_file(vehicle_path, 'scenarios/vehicle.json')
        
        print(times)
        
