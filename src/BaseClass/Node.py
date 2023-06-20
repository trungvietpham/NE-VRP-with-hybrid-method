import copy
from BaseClass.Order import Order, OrderController


class Node:
    def  __init__(self, id, created_at, updated_at, address, code, end_time, latitude, longitude, name, start_time, tpe, capacity, order_hold:list[str] = None, vehicle_list: list[str] = None) -> None:
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.address = str(address)
        self.code = str(code)
        self.start_time = int(start_time)
        self.end_time = int(end_time)
        self.name = str(name)
        self.type = tpe
        # if type(capacity) is int or type(capacity) is float: self.capacity = [capacity]
        if type(capacity) is None: self.capacity = 0
        else: self.capacity = capacity
        if order_hold is None: self.order_hold = []
        else: self.order_hold = order_hold
        if vehicle_list is None: self.vehicle_list: list[str] = []
        else: self.vehicle_list = vehicle_list
    
    def get_code(self) -> str:
        # print('Lấy code của node')
        return self.code
    
    def _add_order_hold(self, order_code: str) -> None:
        self.order_hold.append(order_code)
        return
    
    def _remove_order_hold(self, order_code: str) -> None:
        if order_code in self.order_hold:    
            # del self.order_hold[order_code]
            # self.order_hold.remove(order_code)
            self.order_hold = set(self.order_hold)
            self.order_hold.discard(order_code)
            self.order_hold = list(self.order_hold)
            # self.order_hold.discard()
        return 
    
    def update_order_hold(self, order_code, type: str) -> None:
        '''
        type: add/remove
        '''
        if type == 'add': self._add_order_hold(order_code)
        elif type == 'remove': self._remove_order_hold(order_code)
        return
    
    def get_order_hold(self) -> list[str]:
        '''
        Lấy code của các order nằm trong node này
        '''
        
        return self.order_hold
    
    def get_location(self):
        return self.latitude, self.longitude
    
    def add_vehicle(self, vehicle_code: str) -> None:
        self.vehicle_list.append(vehicle_code)
        return 
    
    def get_total_weight(self, order_controller: OrderController):
        '''
        Lấy khối lượng của các đơn ở điểm
        '''
        res = 0
        for code in self.order_hold:
            res += order_controller.get_order(code).weight
        return res
    
    def to_vector(self):
        return [self.latitude, self.longitude, self.start_time, self.end_time]
    def print(self) -> None:
        for item in self.__dict__.items():
            print(f"{item[0]}: {item[1]}")
        return

class NodeController:
    def __init__(self) -> None:
        self.node_dict: dict[str, Node] = {}
    
    def add(self, node: Node) -> None:
        # print('Thêm 1 node vào nodeController')
        if node.code not in self.node_dict.keys(): self.node_dict[node.code] = node
        return
    
    def remove(self, node_code: str) -> None:
        # print('Xóa 1 node khỏi nodeController')
        if node_code in self.node_dict.keys():
            del self.node_dict[node_code]
        return

    def length(self) -> int: 
        return len(self.node_dict)
    
    def get_node(self, code: str) -> Node:
        if code not in self.node_dict.keys(): return None
        return self.node_dict[code]
    
    def get_node_dict(self) -> dict[str, Node]:
        return self.node_dict
    
    def get_code_list(self) -> list[str]:
        # print('\tLấy thông tin code các node')
        return list(self.node_dict.keys())
    
    def get_order_dict(self) -> dict[str, list[str]]:
        res = {}
        for code, node in self.node_dict.items():
            print(len(node.get_order_hold()))
            input('...')
            if len(node.order_hold) > 0: 
                print('In if')
                res[code] = node.get_order_hold().copy()
        print(res)
        return res
    
    def update_order_hold(self, node_code, order_code, type) -> None:
        '''
        Update trạng thái `type` của order có code là `order_code` trong `node_code`\n
        type: 'add' or 'remove'
        '''
        if node_code not in self.node_dict: 
            return
        self.node_dict[node_code].update_order_hold(order_code, type)
        # if type == 'add':
        # print(self.node_dict[node_code].order_hold)
        # input('..')
        return
    
    def copy(self):
        res = NodeController()
        for code in self.node_dict:
            res.add(copy.deepcopy(self.node_dict[code]))
        return res
    