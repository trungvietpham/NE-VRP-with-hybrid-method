import numpy as np
from BaseClass.Cluster import Cluster, ClusterController
from BaseClass.Correlation import CorrelationController
from BaseClass.Node import Node, NodeController
from BaseClass.Order import Order, OrderController
from BaseClass.Vehicle import VehicleController
from sklearn.cluster import KMeans
# from KMeans import KMeans
from Phase import Phase
from TSP import TSP

class Phase1(Phase):
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: CorrelationController, node_contain_vehicle: NodeController) -> None:
        super().__init__(vehicle_controller, order_controller, correlation, node_contain_vehicle)
    
    def find_nearest_node(self, center, node_list: NodeController) -> Node:
        '''
        Tìm node gần với center nhất
        '''
        # print('\tTìm node gần với center nhất')
        
        all_node = list(node_list.get_node_dict().values())
        dis = []
        for node in all_node:
            # print(f"{np.array(node.get_location())}, {np.array(center)}")
            dis.append(np.linalg.norm(np.array(node.get_location()) - np.array(center)))
        return all_node[int(np.argmin(dis))]
    
    def cluster_phase(self, n_clusters:int, node_controller: NodeController) -> ClusterController:
        cluster_controller = ClusterController()
        # print(node_controller.length())
        node_location = self.get_node_location(node_controller)
        # print(node_location)
        # input('Stop')
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
        
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController, output_filename = None):
        print(f'Bắt đầu phase 1')
        start_node = start_node_controller.copy()
        start_node = self.update_order(start_node, self.order_controller)
        start_node_code_list = self.get_code_list_from_order('start')
        source_node_controller = self.get_node_set(start_node, start_node_code_list)
        dest_node_controller = end_node_controller.copy()
        print(source_node_controller.node_dict.keys())
        input('.....')
        cluster_controller = self.cluster_phase(2, source_node_controller)


        for c in cluster_controller.get_cluster_dict().values():
            # Tìm nearest node có thể điều xe được
            nearest_node = self.find_nearest_node(c.get_center(), self.node_contain_vehicle)
            distance_matrix = self.get_distance_matrix([nearest_node.get_code()] + c.get_list_node_code())
            route = TSP().fit(distance_matrix, algo='bitmasking')
            return_node = self.find_nearest_node(source_node_controller.get_node(self.reverse[int(route[-1])]).get_location(), dest_node_controller) 
            print('Update: ')
            for i in route: 
                if i == 0: 
                    continue
                else: 
                    node_controller = source_node_controller
                    node = source_node_controller.get_node(self.reverse[i])
                order_code_list: list[str] = node.get_order_hold()
                if len(order_code_list) == 0: continue
                for order_code in order_code_list:
                    self.order_controller.update_order_state(order_code, return_node.get_code())
                    dest_node_controller.update_order_hold(node.get_code(), order_code, 'add')
                    
        print('Kết thúc phase 1')
        for node in list(dest_node_controller.get_node_dict().values()):
            if len(node.order_hold) > 0: 
                print(f"{node.get_code()}: {node.order_hold}")
                input('Order hold')
        if output_filename is not None:
            phase_data = self.get_phase_data(dest_node_controller)
            self.output_to_json(phase_data, output_filename)
        return self.order_controller
