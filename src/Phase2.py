from BaseClass.Node import NodeController
from BaseClass.Order import OrderController
from BaseClass.Vehicle import VehicleController
from Phase import Phase
from TSP import TSP

class Phase2(Phase):
    def __init__(self, vehicle_controller: VehicleController, order_controller: OrderController, correlation: dict) -> None:
        super().__init__(vehicle_controller, order_controller, correlation)
        
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController):
        print('Bắt đầu phase 2')
        start_node_code_list = self.get_code_list_from_order('start')
        source_node_controller = self.get_node_set(start_node_controller, start_node_code_list)
        
        for node in source_node_controller.get_node_dict().values():
            dest_node_controller = self.get_node_set(end_node_controller, node.get_order_hold().get_order_state())
            distance_matrix = self.get_distance_matrix(dest_node_controller.get_code_list())
            route = TSP().fit(distance_matrix, algo='bitmasking')
            
            # Cập nhật trạng thái đơn hàng và trạng thái giữ hàng của node
            for i in route:
                node = dest_node_controller.get_node(self.reverse[i])
                
        print('Kết thúc phase 2')
        