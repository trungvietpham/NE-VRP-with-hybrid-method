import numpy as np
from BaseClass.Cluster import Cluster, ClusterController
from BaseClass.Correlation import CorrelationController
from BaseClass.Node import Node, NodeController
from BaseClass.Order import OrderController
from BaseClass.Vehicle import VehicleController
from sklearn.cluster import KMeans
# from KMeans import KMeans
from Phase import Phase
from TSP import TSP

class Phase1(Phase):
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: CorrelationController) -> None:
        super().__init__(vehicle_controller, order_controller, correlation)
    
    def find_nearest_node(self, center, node_list: NodeController) -> Node:
        '''
        Tìm node gần với center nhất
        '''
        print('\tTìm node gần với center nhất')
        
        all_node = list(node_list.get_node_dict().values())
        dis = []
        for node in all_node:
            dis.append(np.linalg.norm(np.array(node.get_location()) - np.array(center)))
        return all_node[int(np.argmin(dis))]
    
    def cluster_phase(self, n_clusters:int, node_controller: NodeController) -> ClusterController:
        cluster_controller = ClusterController()
        node_location = self.get_node_location(node_controller)
        clustering_model = KMeans(n_clusters)
        clustering_model.fit(node_location)
        output = clustering_model.predict(node_location)
        center = clustering_model.cluster_centers_.copy()
        cluster_list : list[Cluster] = []
        for i in range(n_clusters):
            cluster_list.append(Cluster(center[i]))
        
        for i, c in enumerate(output):
            cluster_list[int(c)].add_node(node_controller.get_node(self.code_map[i]))
        
        for i in range(n_clusters):
            cluster_controller.add(cluster_list[i])
        return cluster_controller
        
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController):
        print('Bắt đầu phase 1')
        start_node_code_list = self.get_code_list_from_order('start')
        source_node_controller = self.get_node_set(start_node_controller, start_node_code_list)
        dest_node_controller = self.get_node_set(end_node_controller, code_list=None)
        cluster_controller = self.cluster_phase(dest_node_controller.length(), source_node_controller)
        
        
        for c in cluster_controller.get_cluster_dict().values():
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
