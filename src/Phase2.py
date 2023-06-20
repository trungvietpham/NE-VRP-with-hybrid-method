from BaseClass.Node import NodeController
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
    
    def execute(self, start_node_controller:NodeController, end_node_controller:NodeController, output_filename = None):
        print('Bắt đầu phase 2')
        order_path = self.get_order_path(self.order_controller, self.support_order_controller)
        all_node_path = self.get_all_node_set(order_path)
        
        for node_code, path in all_node_path.items():
            distance_matrix = self.get_distance_matrix([node_code] + path)
            if len(distance_matrix) < 20: algo = 'bitmasking'
            else: algo = 'local_search'
            route = TSP().fit(distance_matrix, algo=algo)
            # Cập nhật trạng thái đơn hàng và trạng thái giữ hàng của node
            print('Update')
            for code, path in order_path.items():
                self.order_controller.update_order_state(code, path[1])
        print('Kết thúc phase 2')
        if output_filename is not None: 
            phase_data = self.get_phase_data()
            self.output_to_json(phase_data, output_filename)
        
        return self.order_controller
        