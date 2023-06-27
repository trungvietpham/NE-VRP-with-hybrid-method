import numpy as np
from sklearn import preprocessing
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
            candidate_vector = np.array(node.to_vector()).reshape(1, -1)
            # print(candidate_vector)
            # input()
            candidate_vector = self.scaler.transform(candidate_vector)
            # print(center)
            # input()
            center_vector = self.scaler.transform(np.array(center).reshape(1, -1))
            # print(f"{candidate_vector}, {center_vector}")
            # input()
            dis.append(np.linalg.norm(candidate_vector - center_vector))
        # print(dis)
        return all_node[int(np.argmin(dis))]
    
    def cluster_phase(self, n_clusters:int, node_controller: NodeController) -> ClusterController:
        cluster_controller = ClusterController()
        node_location = self.get_node_location(node_controller)
        node_tw = self.get_time_window(node_controller)
        
        input_clustering_array = np.append(node_location, node_tw, axis=1)
        # print(f"Input array for clustering: \n{input_clustering_array}")
        # input()
        # Min max scaler data
        self.scaler = preprocessing.MinMaxScaler()
        input_clustering_array = self.scaler.fit_transform(input_clustering_array)
        # print(f"{self.scaler.data_min_} - {self.scaler.data_max_}")
        # input()
        clustering_model = KMeans(int(n_clusters))
        # if n_clusters > 1: 
        clustering_model.fit(input_clustering_array)
        output = clustering_model.predict(input_clustering_array)
        center = self.scaler.inverse_transform(clustering_model.cluster_centers_.copy())
        # else: 
        #     output = [0 for i in range(len(node_location))] 
        #     center = [[1,1]]
        cluster_list : list[Cluster] = []
        for i in range(n_clusters):
            cluster_list.append(Cluster(center[i]))
        
        for i, c in enumerate(output):
            cluster_list[int(c)].add_node(node_controller.get_node(self.code_map[i]))
        for i in range(n_clusters):
            cluster_controller.add(cluster_list[i])
        return cluster_controller
        
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController, phase_data, reverse = False):
        
        print(f'Bắt đầu phase 1')
        start_node = start_node_controller.copy()
        start_node = self.update_order(start_node, self.order_controller)
        start_node_code_list = self.get_code_list_from_order('start')
        source_node_controller = self.get_node_set(start_node, start_node_code_list)
        if source_node_controller.length() == 0:
            # print(f"Found length 0")
            # self.order_controller.print()
            # input('awue')
            return self.order_controller, phase_data
        
        dest_node_controller = end_node_controller.copy()
        # n_clusters = dest_node_controller.length()
        n_clusters = int(source_node_controller.length() // 15 + 1)
        # while True: 
        #     if n_clusters == 0: n_clusters = 1
        #     if n_clusters <= source_node_controller.length(): break
        #     n_clusters/=5
        #     n_clusters = int(n_clusters)
            
        cluster_controller = self.cluster_phase(int(n_clusters), source_node_controller)
        vehicle_route = {}

        print('Start TSP phase')
        for c in cluster_controller.get_cluster_dict().values():
            # Tính toán khối lượng cần tải trọng 1 lượt
            total_weight = c.get_total_weight(self.order_controller)
            # Tìm nearest node có thể điều xe được
            node_contain_vehicle = self.node_contain_vehicle.copy()
            
            if not reverse:
                while True:
                    nearest_node = self.find_nearest_node(c.get_center(), node_contain_vehicle)
                    # Lấy các xe để chạy:
                    vehicle_list = self.get_route_vehicle(nearest_node, total_weight)
                    if node_contain_vehicle.length() == 0: 
                        print('Bài toán không khả thi')
                        exit(-1)
                    if vehicle_list is not None: break 
                    node_contain_vehicle.remove(nearest_node.get_code())
                v = vehicle_list[0]
            
            else:
                target_node_controller = end_node_controller.copy()
                while True:
                    target_node_controller.print()
                    # input('seijs')
                    nearest_node = self.find_nearest_node(c.get_center(), target_node_controller)
                    # Lấy các xe để chạy:
                    vehicle_list = self.get_route_vehicle(nearest_node, total_weight)
                    if node_contain_vehicle.length() == 0: 
                        print('Bài toán không khả thi')
                        exit(-1)
                    if vehicle_list is not None: break 
                    target_node_controller.remove(nearest_node.get_code())
                v = vehicle_list[0]
            
            # Loại bỏ node_code trong c
            node_code = nearest_node.get_code()
            path = c.get_list_node_code()
            if node_code in path: path.remove(node_code)
            distance_matrix = self.get_distance_matrix([nearest_node.get_code()] + c.get_list_node_code())
            if len(distance_matrix) < 20: algo = 'bitmasking'
            else: algo = 'local_search'
            route = TSP().fit(distance_matrix, algo=algo)
            return_node = self.find_nearest_node(source_node_controller.get_node(self.reverse[int(route[-1])]).to_vector(), dest_node_controller) 
            print('Update: ')
            if v not in vehicle_route: vehicle_route[v] = []
            for i in route: 
                vehicle_route[v].append(self.reverse[i])
                if i == 0: 
                    continue
                else: 
                    node_controller = source_node_controller
                    node = source_node_controller.get_node(self.reverse[i])
                order_code_list: list[str] = node.get_order_hold()
                if len(order_code_list) == 0: continue
                for order_code in order_code_list:
                    # Update thông tin trạng thái đơn hàng và trang thái giữ hàng của node
                    self.order_controller.update_order_state(order_code, return_node.get_code(), v)
                    source_node_controller.update_order_hold(node.get_code(), order_code, 'remove')
                    dest_node_controller.update_order_hold(return_node.get_code(), order_code, 'add')
                    self.vehicle_cotroller.update_vehicle_state(v, return_node.get_code())
            vehicle_route[v].append(return_node.get_code())
        print('Kết thúc phase 1')
        if reverse: phase_data = self.update_phase_data(dest_node_controller, vehicle_route=vehicle_route, phase_data=phase_data, skip_node=True)
        else: phase_data = self.update_phase_data(dest_node_controller, vehicle_route=vehicle_route, phase_data=phase_data)
        return self.order_controller, phase_data
