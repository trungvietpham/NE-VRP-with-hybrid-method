import numpy as np
import pandas as pd
import sys
sys.path.append("")
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
        print('\tLoad thông tin về đội xe: start ')
        
        data = pd.read_csv(self.vehicle_file_name, sep='\t')
        vehicle_controller = VehicleController()
        for i in range(len(data)):
            line = data.iloc[i]
            vehicle_controller.add(Vehicle(int(line['code']), line['created_at'], line['updated_at'], 
                                           line['available'], float(line['average_fee_transport']),
                                           float(line['average_gas_consume']), float(line['average_velocity']),
                                           line['driver_name'], 
                                           line['gas_price'], line['height'],
                                           line['length'], line['max_capacity'],
                                           line['max_load_weight'], line['max_velocity'],
                                           line['min_velocity'], line['name'], line['type'], 
                                           line['width'], line['vehicle_cost'], 
                                           str(line['manager_node']), str(line['current_node'])))
        print('\tLoad thông tin về đội xe: done')
        return vehicle_controller
    
    def load_node(self) -> NodeController:
        '''
        Load thông tin các node lên
        '''
        print('\tLoad thông tin các node: start')
        data = pd.read_csv(self.node_file_name, sep='\t')
        node_controller = NodeController()
        for i in range(len(data)):
            line = data.iloc[i]
            if line['type'] in ['GD2', 'GD3']: type = 'GD2'  
            else: type = 'GD1'
            node_controller.add(Node(line['created_at'], line['updated_at'], str(line['address']),
                                     str(line['code']), int(line['end_time']), float(line['latitude']), 
                                     str(line['longitude']), str(line['name']), int(line['start_time']), 
                                     type, line['capacity'], int(line['province_code']), int(line['district_code'])))
            
        print('\tLoad thông tin các node: done')
        return node_controller
    
    def load_order(self) -> OrderController:
        print('\tLoad thông tin về các đơn hàng: start')
        data = pd.read_csv(self.order_file_name, sep='\t')
        order_controller = OrderController()
        for i in range(len(data)):
            line = data.iloc[i]
            order_controller.add(Order(line['created_at'], line['updated_at'],
                                       line['capacity'], str(line['code']), int(line['delivery_after_time']),
                                       int(line['delivery_before_time']), line['delivery_mode'],
                                       line['order_value'], line['time_service'], line['time_loading'], 
                                       line['weight'], str(line['receiver_code']), str(line['sender_code']) ))
        
        print('\tLoad thông tin về các đơn hàng: done')
        return order_controller
    
    def load_correlation(self) -> CorrelationController:
        '''
        Load ma trận khoảng cách lưu vào 1 dict
        '''
        print('\tLoad ma trận khoảng cách: start')
        data = pd.read_csv(self.correlation_file_name, sep='\t')
        correlation_controller = CorrelationController()
        for i in range(len(data)):
            line = data.iloc[i]
            corr = Correlation(line['id'], line['created_at'], line['updated_at'], 
                                                   line['distance'], str(int(float(line['from_node_code']))), line['from_node_id'],
                                                   line['from_node_name'], line['from_node_type'], line['risk_probability'],
                                                   line['time'], str(int(float(line['to_node_code']))), 
                                                   line['to_node_id'], line['to_node_name'], 
                                                   line['to_node_type'])
            correlation_controller.add(corr)
        print('\tLoad ma trận khoảng cách: done')
        return correlation_controller

    
    def order_hierachical_by_province(self, all_order: OrderController, sender_flag = True) -> dict[str, OrderController]:
        res: dict[str, OrderController] = {}
        if sender_flag: tpe = 'depot_id'
        else: tpe = 'customer_id'
        for order in list(all_order.get_order_dict().values()):
            if self.province_map[order.__getattribute__(tpe)] not in res: res[self.province_map[order.__getattribute__(tpe)]] = OrderController()
            res[self.province_map[order.__getattribute__(tpe)]].add(order)
            
        return res
    
    def update_province_map(self, node_controller: NodeController): 
        if not hasattr(self, 'province_map'): self.province_map = {}
        
        for node in list(node_controller.get_node_dict().values()):
            self.province_map[node.code] = node.province_code
        return
    
    def update_order_state(self, all_order: OrderController, by='start'):
        '''
        by: 'start' or 'end'
        '''
        if by == 'start': 
            for code, order in all_order.get_order_dict().items():
                all_order.update_order_state(code, order.get_start_code())
        if by == 'end':
            for code, order in all_order.get_order_dict().items():
                all_order.update_order_state(code, order.get_end_code(), remove_flag=True)
                
        return all_order
    
    def add_node_vehicle_list(self, all_node: NodeController, all_vehicle: VehicleController) -> tuple[NodeController, VehicleController]: 
        for vehicle in list(all_vehicle.get_vehicle_dict().values()):
            # print(vehicle.manager_node)
            all_node.get_node(vehicle.manager_node).add_vehicle(vehicle.id)
        return all_node, all_vehicle
    
    def hierarchical_node(self, node_controller: NodeController) -> dict[int, dict[str, NodeController]]:
        print('\tPhân cấp các node đầu vào theo node.type: start')
        all_hierarchical:dict[int, dict[str, NodeController]] = {}
        for _, node in node_controller.get_node_dict().items():
            province_code = int(node.province_code)
            if province_code not in all_hierarchical: 
                all_hierarchical[province_code] = {}
            if node.type not in all_hierarchical[province_code]: all_hierarchical[province_code][node.type] = NodeController()
            all_hierarchical[province_code][node.type].add(node)
        print('\tPhân cấp các node đầu vào theo node.type: done')
        return all_hierarchical
    
    def hierarchical_vehicle(self, vehicle_controller: VehicleController) -> dict[int, VehicleController]: 
        all_hierarchical: dict[int, VehicleController] = {}
        for _, vehicle in vehicle_controller.get_vehicle_dict().items():
            province_code = self.province_map[vehicle.manager_node]
            if province_code not in all_hierarchical: all_hierarchical[province_code] = VehicleController()
            all_hierarchical[province_code].add(vehicle)
        return all_hierarchical
    
    def get_all_vehicle_node(self, all_node: NodeController) -> dict[int, NodeController]:
        '''
        Lấy ra thông tin các node có chứa xe 
        '''
        return_node_controller: dict[int, NodeController] = {}
        for node in list(all_node.get_node_dict().values()):
            if len(node.vehicle_list) > 0:
                province_code = node.province_code
                if province_code not in return_node_controller: return_node_controller[province_code] = NodeController()
                return_node_controller[province_code].add(node)
        return return_node_controller
    
    def concatenate(self, a_dict: dict[int, VehicleController|NodeController]):
        to_list = list(a_dict.values())
        res = to_list[0]
        # res.print()
        for v_c in to_list[1:]: 
            res.__add__(v_c)
        return res
    
    def execute(self):
        print('Chạy các bước chuẩn bị dữ liệu: start')
        all_node = self.load_node()
        self.update_province_map(all_node)
        all_vehicle = self.load_vehicle()
        all_order = self.load_order()
        correlation = self.load_correlation()
        all_node, all_vehicle = self.add_node_vehicle_list(all_node, all_vehicle)
        hierarchical_node_contain_vehicle = self.get_all_vehicle_node(all_node)
        hierarchical_node = self.hierarchical_node(all_node)
        hierarchical_vehicle = self.hierarchical_vehicle(all_vehicle)
        
        # Export dữ liệu phân cấp ra
        print('Chạy các bước chuẩn bị dữ liệu: done')

        
        return [hierarchical_node, hierarchical_vehicle, all_order, correlation, hierarchical_node_contain_vehicle]
        
        # end_node_controller = self.get_node_set(all_node, type_list=)