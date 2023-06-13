from abc import abstractmethod
import os
import json

import numpy as np
from BaseClass.Correlation import CorrelationController
from BaseClass.Vehicle import VehicleController
from BaseClass.Order import OrderController
from BaseClass.Node import NodeController
class Phase:
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: CorrelationController, node_contain_vehicle: NodeController) -> None:
        self.vehicle_cotroller = vehicle_controller
        self.order_controller = order_controller
        self.correlation = correlation
        self.node_contain_vehicle = node_contain_vehicle

    def get_code_list_from_order(self, type: str) -> list:
        '''
        type: 'start' hoặc 'end' \n
        Nếu là 'start' thì lấy vị trí hiện tại của đơn hàng \n
        Nếu là 'end' thì lấy vị trí đích của đơn hàng \n
        '''
        valid_list = ['start', 'end']
        assert type in valid_list, f'type must be in {valid_list}'
        # print('\tLấy thông tin về code từ các order')
        
        res = []
        if type == 'start':
            for order_code, order in self.order_controller.get_order_dict().items():
                res.append(order.state[-1])
        if type == 'end':
            for order_code, order in self.order_controller.get_order_dict().items():
                res.append(order.customer_id)
        return res
    
    def get_node_set(self, all_node: NodeController, code_list: list) -> NodeController:
        '''
        Lấy các node có code trong code_list.
        Nếu code_list = None thì trả về all_node
        '''
        print('\tLấy tập hợp các node cần gửi hàng/ giao hàng')
        if code_list is None: return all_node
        valid_node_code = all_node.get_code_list()
        res = NodeController()
        for code in code_list: 
            # print(code)
            if code in valid_node_code:
                res.add(all_node.get_node(code))
        return res
    
    def get_node_location(self, node_controller: NodeController) -> np.ndarray:
        location = []
        self.code_map = []
        for _, node in node_controller.get_node_dict().items():
            location.append(node.get_location())
            self.code_map.append(node.code)
        self.code_map = np.array(self.code_map)
        return np.array(location)
    
    def get_distance_matrix(self, code_list: list[str]) -> np.ndarray:
        '''
        Sử dụng self.correlation để lấy ma trận khoảng cách của các điểm trong node_list
        code_list: danh sách code của các node
        '''
        print(code_list)
        self.reverse = []
        self.reverse = code_list.copy()
        distance_matrix = np.zeros((len(code_list), len(code_list)))
        for i in range(len(code_list)):
            for j in range(len(code_list)):
                corr = self.correlation.get_correlation(code_list[i], code_list[j])
                if corr is None: distance_matrix[i][j] = 1e9
                else: 
                    distance_matrix[i][j] = corr.distance
                    # print(f'Corr = {distance_matrix[i][j]}')
        
        # Ko xét quãng đường quay về <=> distance_matrix[i,0] = 0
        for i in range(len(code_list)):
            distance_matrix[i][0] = 0
        return np.array(distance_matrix)
    
    def update_order(self, all_node: NodeController, all_order: OrderController) -> NodeController:
        '''
        Cập nhật thông tin trạng thái giữ hàng của từng node
        '''
        valid_node = all_node.get_code_list()
        for order in list(all_order.get_order_dict().values()):
            if order.get_current_state() in valid_node:
                all_node.update_order_hold(order.get_current_state(), order.get_code(), 'add')
        return all_node
    
    def get_phase_data(self, node_controller: NodeController = None):
        res = {'order': {}, 'node': {}}
        res['order'] = self.order_controller.get_order_state()
        for order_code, node_code in res['order'].items():
            if node_code not in res['node']: res['node'][node_code] = []
            res['node'][node_code].append(order_code) 
        return res
    
    def output_to_json(self, data, filename): 
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename)) 
        json.dump(data, open(filename, 'w'), indent=4)
        print('Dump data done')
        return
    
    @abstractmethod
    def execute(self):
        pass