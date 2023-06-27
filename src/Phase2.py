import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans
from BaseClass.Cluster import Cluster, ClusterController
from BaseClass.Node import Node, NodeController
from BaseClass.Order import OrderController
from BaseClass.Vehicle import VehicleController
from BaseClass.Correlation import CorrelationController
from Phase import Phase
from TSP import TSP

class Phase2(Phase):
    def __init__(self, vehicle_controller: VehicleController, sender_side_order_controller: OrderController, receiver_side_order_controller: OrderController, correlation: CorrelationController, node_contain_vehicle: NodeController) -> None:
        super().__init__(vehicle_controller, sender_side_order_controller, correlation, node_contain_vehicle)
        self.support_order_controller = receiver_side_order_controller
    
    def get_order_path(self, sender_side_order: OrderController, receiver_side_order: OrderController):
        '''
        Lấy thông tin về điểm GD1 bên gửi và bên nhận
        '''
        res = {}
        for code in sender_side_order.get_order_code():
            res[code] = [sender_side_order.get_order(code).get_current_state(), receiver_side_order.get_order(code).get_current_state()]
        return res
    
    def get_code_list_from_order(self, type: str, order_path: dict[str, list]) -> list:
        res = []
        if type == 'start':
            for code, path in order_path.items():
                if path[0] not in res: 
                    res.append(path[0])
        if type == 'end':
            for code, path in order_path.items():
                if path[1] not in res:
                    res.append(path[1])
        
        return res
    
    def get_all_node_set(self, order_path: dict[str, list]) -> dict[str, list]:
        '''
        Lấy code của các node cần giao hàng từ 1 node hiện tại, bảng giao hàng ở order_path
        '''
        res = {}
        for path in list(order_path.values()):
            if path[0] not in res: res[path[0]] = []
            res[path[0]].append(path[1])
        
        for i in res: 
            res[i] = list(set(res[i]))
        
        return res
    
    def find_nearest_node(self, center, node_list: NodeController) -> Node:
        '''
        Tìm node gần với center nhất
        '''
        
        all_node = list(node_list.get_node_dict().values())
        dis = []
        for node in all_node:
            candidate_vector = np.array(node.to_vector()).reshape(1, -1)
            candidate_vector = self.scaler.transform(candidate_vector)
            center_vector = self.scaler.transform(np.array(center).reshape(1, -1))
            dis.append(np.linalg.norm(candidate_vector - center_vector))
        return all_node[int(np.argmin(dis))]
    
    def cluster_phase_2(self, node_controller: NodeController, path: list[str], start_node_code:str) -> ClusterController:
        cluster_controller = ClusterController()
        node_location = self.get_node_location(node_controller)
        node_tw = self.get_time_window(node_controller)
        
        input_clustering_array = np.append(node_location, node_tw, axis=1)
        # Min max scaler data
        self.scaler = preprocessing.MinMaxScaler()
        input_clustering_array = self.scaler.fit_transform(input_clustering_array)
        # print(start_node_code)
        # node_controller.print()
        # input('asdjw')
        node = node_controller.get_node(start_node_code)
        if node is None: return None
        center = node_controller.get_node(start_node_code).to_vector()
        # else: 
        #     output = [0 for i in range(len(node_location))] 
        #     center = [[1,1]]
        cluster_list : list[Cluster] = []
        cluster_list.append(Cluster(center))
        
        print(f'Path: {path}')
        for code in path:
            node = node_controller.get_node(code)
            if node is None: continue
            cluster_list[0].add_node(node)
        cluster_controller.add(cluster_list[0])
        return cluster_controller
    
    # def cluster_phase(self, n_clusters:int, node_controller: NodeController) -> ClusterController:
    #     cluster_controller = ClusterController()
    #     node_location = self.get_node_location(node_controller)
    #     node_tw = self.get_time_window(node_controller)
        
    #     input_clustering_array = np.append(node_location, node_tw, axis=1)
    #     # print(f"Input array for clustering: \n{input_clustering_array}")
    #     # input()
    #     # Min max scaler data
    #     self.scaler = preprocessing.MinMaxScaler()
    #     input_clustering_array = self.scaler.fit_transform(input_clustering_array)
    #     # print(f"{self.scaler.data_min_} - {self.scaler.data_max_}")
    #     # input()
    #     clustering_model = KMeans(int(n_clusters))
    #     # if n_clusters > 1: 
    #     clustering_model.fit(input_clustering_array)
    #     output = clustering_model.predict(input_clustering_array)
    #     center = self.scaler.inverse_transform(clustering_model.cluster_centers_.copy())
    #     # else: 
    #     #     output = [0 for i in range(len(node_location))] 
    #     #     center = [[1,1]]
    #     cluster_list : list[Cluster] = []
    #     for i in range(n_clusters):
    #         cluster_list.append(Cluster(center[i]))
        
    #     for i, c in enumerate(output):
    #         cluster_list[int(c)].add_node(node_controller.get_node(self.code_map[i]))
    #     for i in range(n_clusters):
    #         cluster_controller.add(cluster_list[i])
    #     return cluster_controller
    
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController, output_filename = None):
        print('Bắt đầu phase 2')
        order_path = self.get_order_path(self.order_controller, self.support_order_controller)
        # print(order_path)
        # input('asdhue')
        all_node_path = self.get_all_node_set(order_path)
        vehicle_route = {}
        
        for node_code, path in all_node_path.items():
            # print(f"{node_code}, {path}")
            # input('ursjgnj')
            cluster = self.cluster_phase_2(start_node_controller.copy(), path, node_code)
            if cluster is None: continue
            c = list(cluster.get_cluster_dict().values())[0]
            
            # Tính toán khối lượng cần tải trọng 1 lượt
            total_weight = c.get_total_weight(self.order_controller)
            
            # Tìm nearest node có thể điều xe được
            node_contain_vehicle = self.node_contain_vehicle.copy()
            
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
            
            # Loại bỏ node_code trong path nếu có
            if node_code in path: path.remove(node_code)
            
            distance_matrix = self.get_distance_matrix([node_code] + path)
            if len(distance_matrix) < 20: algo = 'bitmasking'
            else: algo = 'local_search'
            route = TSP().fit(distance_matrix, algo=algo)
            # Cập nhật trạng thái đơn hàng và trạng thái giữ hàng của node
            print('Update')
            if v not in vehicle_route: vehicle_route[v] = []
            for i in route:
                vehicle_route[v].append(self.reverse[i])
            for code, p in order_path.items():
                # print(path)
                # print(self.order_controller.get_order(code).get_current_state())
                if self.order_controller.get_order(code).get_current_state() in self.reverse:
                    self.order_controller.update_order_state(code, p[1], v)
        print('Kết thúc phase 2')
        if output_filename is not None: 
            phase_data = self.update_phase_data(vehicle_route=vehicle_route)
            self.output_to_json(phase_data, output_filename)
        
        return self.order_controller
        