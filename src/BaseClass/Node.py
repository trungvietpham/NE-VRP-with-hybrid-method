from BaseClass.Order import Order, OrderController


class Node:
    def  __init__(self, latitude, longitude, address, code, start_time, end_time, name, type, capacity, order_hold:OrderController) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.code = code
        self.start_time = start_time
        self.end_time = end_time
        self.name = name
        self.type = type
        self.capacity = capacity
        self.order_hold = order_hold
    
    def get_code(self) -> str:
        print('Lấy code của node')
        return self.code
    
    def _add_order_hold(self, order: Order) -> None:
        print('Thêm order vào danh sách order_hold')
        return
    
    def _remove_order_hold(self, order: Order) -> None:
        print('Xóa order khỏi order_hold')
        return 
    
    def update_order_hold(self, order: Order, type: str) -> None:
        '''
        type: add/remove
        '''
        if type == 'add': self._add_order_hold(order)
        elif type == 'remove': self._remove_order_hold(order)
        return
    
    def get_order_hold(self) -> OrderController:
        return self.order_hold

class NodeController:
    def __init__(self) -> None:
        self.node_dict = {}
    
    def add(self, node: Node) -> None:
        print('Thêm 1 node vào nodeController')
        return

    def length(self) -> int: 
        return len(self.node_dict)
    
    def get_node(self, code: str) -> Node:
        return self.node_dict[code]
    
    def get_node_dict(self) -> dict[str, Node]:
        return self.node_dict
    
    def get_code_list(self):
        print('\tLấy thông tin code các node')
        return