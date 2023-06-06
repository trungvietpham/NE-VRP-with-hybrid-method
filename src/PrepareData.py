import numpy as np
import pandas as pd
from BaseClass.Node import Node, NodeController
from BaseClass.Order import Order, OrderController
from BaseClass.Vehicle import Vehicle, VehicleController
from BaseClass.Correlation import Correlation, CorrelationController

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
        
        data = pd.read_csv(self.vehicle_file_name)
        vehicle_controller = VehicleController()
        for i in range(len(data)):
            line = data.iloc[i]
            vehicle_controller.add(Vehicle(int(line['id']), line['created_at'], line['updated_at'], 
                                           line['available'], float(line['average_fee_transport']),
                                           float(line['average_gas_consume']), float(line['average_velocity']),
                                           line['fixed_cost'], line['driver_name'], 
                                           line['gas_price'], line['height'],
                                           line['length'], line['max_capacity'],
                                           line['max_load_weight'], line['max_velocity'],
                                           line['min_velocity'], line['name'], line['type'], 
                                           line['width'], line['dx_code'], line['vehicle_cost'], 
                                           str(line['manager_node'])))
        return vehicle_controller
    
    def load_node(self) -> NodeController:
        '''
        Load thông tin các node lên
        '''
        print('\tLoad thông tin các node')
        data = pd.read_csv(self.node_file_name)
        node_controller = NodeController()
        for i in range(len(data)):
            line = data.iloc[i]
            node_controller.add(Node(int(line['id']), line['created_at'], line['updated_at'], str(line['address']),
                                     str(line['code']), int(line['end_time']), float(line['latitude']), 
                                     str(line['longitude']), str(line['name']), int(line['start_time']), 
                                     line['type'], line['capacity']))
        return node_controller
    
    def load_order(self) -> OrderController:
        print('\tLoad thông tin về các đơn hàng')
        data = pd.read_csv(self.order_file_name)
        order_controller = OrderController()
        for i in range(len(data)):
            line = data.iloc[i]
            order_controller.add(Order(int(line['id']), line['created_at'], line['updated_at'],
                                       line['capacity'], str(line['code']), int(line['delivery_after_time']),
                                       int(line['delivery_before_time']), line['delivery_mode'], line['intend_receive_time'],
                                       line['order_value'], line['time_service'], line['time_loading'], 
                                       line['weight'], str(line['customer_id']), str(line['depot_id']), line['dx_code']))
            
        return order_controller
    
    def load_correlation(self) -> CorrelationController:
        '''
        Load ma trận khoảng cách lưu vào 1 dict
        '''
        print('\tLoad ma trận khoảng cách')
        data = pd.read_csv(self.correlation_file_name)
        correlation_controller = CorrelationController()
        for i in range(len(data)):
            line = data.iloc[i]
            corr = Correlation(line['id'], line['created_at'], line['updated_at'], 
                                                   line['distance'], line['from_node_code'], line['from_node_id'],
                                                   line['from_node_name'], line['from_node_type'], line['risk_probability'],
                                                   line['time'], line['to_node_code'], 
                                                   line['to_node_id'], line['to_node_name'], 
                                                   line['to_node_type'])
            correlation_controller.add(corr)
        return correlation_controller
    
    def hierarchical_node(self, node_controller: NodeController) -> dict[str, NodeController]:
        print('\tPhân cấp các node đầu vào theo node.type')
        all_hierarchical:dict[str, NodeController] = {}
        for _, node in node_controller.get_node_dict().items():
            if node.type not in all_hierarchical: 
                all_hierarchical[node.type] = NodeController()
            all_hierarchical[node.type].add(node)
            
        return all_hierarchical
    
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