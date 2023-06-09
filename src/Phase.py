from abc import abstractmethod
import os
import json

import numpy as np
from BaseClass.Correlation import CorrelationController
from BaseClass.Vehicle import VehicleController
from BaseClass.Order import OrderController
from BaseClass.Node import Node, NodeController
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
        if code_list is None: return all_node
        valid_node_code = all_node.get_code_list()
        res = NodeController()
        for code in code_list: 
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
    
    def get_time_window(self, node_controller: NodeController) -> np.ndarray:
        tw = []
        for _, node in node_controller.get_node_dict().items():
            tw.append([node.start_time, node.end_time])
        return np.array(tw)
        
    def get_route_vehicle(self, target_node: Node, total_weight):
        vehicle_list = target_node.vehicle_list
        res = []
        current_capacity = 0
        print(f"target node: {target_node.code}, vehicle list: {vehicle_list}, total weight: {total_weight}")
        while True:
            if len(vehicle_list) == 0: return None
            best = -1
            current_v = ''
            for v in vehicle_list:
                if self.vehicle_cotroller.get_vehicle(v).max_capacity > best: 
                    best = self.vehicle_cotroller.get_vehicle(v).max_capacity
                    current_v = v
            current_capacity+=best
            res.append(current_v)
            if current_capacity>=total_weight: break
            else: print(f"current capa: {current_capacity}, total weight: {total_weight}")
            vehicle_list.remove(current_v)
            best=0
            
        if current_capacity<total_weight: return None
        return res
    
    def get_distance_matrix(self, code_list: list[str]) -> np.ndarray:
        '''
        Sử dụng self.correlation để lấy ma trận khoảng cách của các điểm trong node_list
        code_list: danh sách code của các node
        '''
        # print(code_list)
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
        
        # print(code_list)
        # print(distance_matrix)
        # input('asdwqwe')
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
    
    def update_phase_data(self, node_controller: NodeController = None, vehicle_route = None, phase_data = None, skip_node = False):
        res = phase_data
        if res is None: res = {}
        if 'order' not in res: res['order'] = {}
        if 'node' not in res and not skip_node: res['node'] = {}
        if 'vehicle' not in res: res['vehicle'] = {}
        # print(self.order_controller.get_order_path())
        res['order'].update(self.order_controller.get_order_path())
        if not skip_node:
            for order_code, node_code in res['order'].items():
                node_code = node_code.split('->')[0].strip()
                if node_code not in res['node']: res['node'][node_code] = []
                res['node'][node_code].append(order_code) 
        
        if vehicle_route is not None: 
            res['vehicle'].update(vehicle_route)
        
        return res
    
    def output_to_json(self, data, filename): 
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename)) 
        # print(data.keys())
        json.dump(data, open(filename, 'w'), indent=4)
        print('Dump data done')
        return
    
    @abstractmethod
    def execute(self):
        pass