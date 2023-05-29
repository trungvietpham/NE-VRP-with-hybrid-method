from abc import abstractmethod

import numpy as np
from BaseClass.Vehicle import VehicleController
from BaseClass.Order import OrderController
from BaseClass.Node import NodeController
class Phase:
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: dict) -> None:
        self.vehicle_cotroller = vehicle_controller
        self.order_controller = order_controller
        self.correlation = correlation
    
    def get_code_list_from_order(self, type: str) -> list:
        print('\tLấy thông tin về code từ các order')
        return ['A', 'list', 'of', 'node', 'code']
    
    def get_node_set(self, all_node: NodeController, code_list: list) -> NodeController:
        '''
        Lấy các node có code trong code_list.
        Nếu code_list = None thì trả về all_node
        '''
        print('\tLấy tập hợp các node cần gửi hàng/ giao hàng')
        return NodeController()
    
    def get_distance_matrix(self, node_list: list) -> np.ndarray:
        '''
        Sử dụng self.correlation để lấy ma trận khoảng cách của các điểm trong node_list
        '''
        print('\tLấy ra thông tin về ma trận khoảng cách giữa các node trong node_list')
        self.reverse = ['id1']
        return np.array([1])
    
    @abstractmethod
    def execute(self):
        pass