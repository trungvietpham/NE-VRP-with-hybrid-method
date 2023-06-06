from abc import abstractmethod

import numpy as np
from BaseClass.Correlation import CorrelationController
from BaseClass.Vehicle import VehicleController
from BaseClass.Order import OrderController
from BaseClass.Node import NodeController
class Phase:
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: CorrelationController) -> None:
        self.vehicle_cotroller = vehicle_controller
        self.order_controller = order_controller
        self.correlation = correlation
    
    def get_code_list_from_order(self, type: str) -> list:
        '''
        type: 'start' hoặc 'end' \n
        Nếu là 'start' thì lấy vị trí hiện tại của đơn hàng \n
        Nếu là 'end' thì lấy vị trí đích của đơn hàng \n
        '''
        valid_list = ['start', 'end']
        assert type in valid_list, f'type must be in {valid_list}'
        print('\tLấy thông tin về code từ các order')
        
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
        res = NodeController()
        for code in code_list: 
            res.add(all_node.get_node(code))
        return res
    
    def get_node_location(self, node_controller: NodeController) -> np.ndarray:
        location = []
        self.code_map = []
        for _, node in node_controller.get_node_dict().items():
            location.append(node.get_location())
            self.code_map.append(node.code)
        return np.array(location)
    
    def get_distance_matrix(self, code_list: list[str]) -> np.ndarray:
        '''
        Sử dụng self.correlation để lấy ma trận khoảng cách của các điểm trong node_list
        code_list: danh sách code của các node
        '''
        print('\tLấy ra thông tin về ma trận khoảng cách giữa các node trong node_list')
        self.reverse = code_list.copy()
        distance_matrix = np.zeros((len(code_list), len(code_list)))
        for i in range(len(code_list)):
            for j in range(len(code_list)):
                corr = self.correlation.get_correlation(code_list[i], code_list[j])
                if corr is None: distance_matrix[i][j] = 1e9
                else: distance_matrix[i][j] = corr.distance
        
        # Ko xét quãng đường quay về <=> distance_matrix[i,0] = 0
        for i in range(len(code_list)):
            distance_matrix[i][0] = 0
        return np.array(distance_matrix)
    
    @abstractmethod
    def execute(self):
        pass