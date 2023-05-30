import numpy as np
from BaseClass.Node import NodeController
from BaseClass.Order import OrderController
from BaseClass.Vehicle import VehicleController

class PrepareData():
    def __init__(self, vehicle_fname, node_fname, correlation_fname, order_fname) -> None:
        self.vehicle_file_name = vehicle_fname
        self.node_file_name = node_fname
        self.correlation_file_name = correlation_fname
        self.order_file_name = order_fname
    
    def load_vehicle(self) -> VehicleController:
        '''
        Load thông tin về các xe
        '''
        print('\tLoad thông tin về đội xe ')
        return
    
    def load_node(self) -> NodeController:
        '''
        Load thông tin các node lên
        '''
        print('\tLoad thông tin các node')
        return
    
    def load_order(self) -> OrderController:
        print('\tLoad thông tin về các đơn hàng')
        return
    
    def load_correlation(self) -> dict:
        '''
        Load ma trận khoảng cách lưu vào 1 dict
        '''
        print('\tLoad ma trận khoảng cách')
        return
    
    def hierarchical_node(self, node_controller: NodeController) -> dict[str, NodeController]:
        print('\tPhân cấp các node đầu vào theo node.type')
        return
    
    def execute(self):
        print('Chạy các bước chuẩn bị dữ liệu')
        all_node = self.load_node()
        all_vehicle = self.load_vehicle()
        all_order = self.load_order()
        correlation = self.load_correlation()
        hierarchical_node = self.hierarchical_node(all_node)
        
        # Export dữ liệu phân cấp ra
        print('Đã chuẩn bị xong dữ liệu')
        
        return hierarchical_node, all_vehicle, all_order, correlation
        
        # end_node_controller = self.get_node_set(all_node, type_list=)