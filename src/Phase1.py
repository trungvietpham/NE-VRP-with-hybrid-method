import numpy as np
from BaseClass.Cluster import Cluster
from BaseClass.Node import Node, NodeController
from BaseClass.Order import OrderController
from BaseClass.Vehicle import VehicleController
from KMeans import KMeans
from Phase import Phase
from TSP import TSP

class Phase1(Phase):
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: dict) -> None:
        super().__init__(vehicle_controller, order_controller, correlation)
    
    def find_nearest_node(self, center, node_list: NodeController) -> Node:
        '''
        Tìm node gần với center nhất
        '''
        print('\tTìm node gần với center nhất')
        return
    
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController):
        print('Bắt đầu phase 1')
        start_node_code_list = self.get_code_list_from_order('start')
        source_node_controller = self.get_node_set(start_node_controller, start_node_code_list)
        clustering_model = KMeans(3)
        output = clustering_model.fit()
        dest_node_controller = self.get_node_set(end_node_controller, code_list=None)
        
        for c in output.get_cluster_dict().values():
            nearest_node = self.find_nearest_node(c.get_center(), source_node_controller)
            distance_matrix = self.get_distance_matrix([nearest_node.get_code] + c.get_list_node_code())
            route = TSP().fit(distance_matrix, algo='bitmasking')
            return_node = self.find_nearest_node()
            for i in route: 
                node = source_node_controller.get_node(self.reverse[i])
                node.update_order_hold()
                for order in node.get_order_hold().get_order_dict():
                    order.update_state()
        
        print('Kết thúc phase 1')
        return 
