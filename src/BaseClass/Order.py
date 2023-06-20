import copy
class Order:
    def __init__(
        self, 
        id, 
        created_at, 
        updated_at, 
        capacity, 
        code, 
        delivery_after_time, 
        delivery_before_time, 
        delivery_mode, 
        intend_receive_time, 
        order_value, 
        time_service, 
        time_loading, 
        weight, 
        customer_id, 
        depot_id, 
        dx_code
        ) -> None:
        self.id = id
        self.create_at = created_at
        self.update_at = updated_at
        self.capacity = capacity
        self.code = code
        self.delivery_after_time = int(delivery_after_time)
        self.delivery_before_time = int(delivery_before_time)
        self.delivery_mode = delivery_mode 
        self.intend_receive_time = intend_receive_time 
        self.order_value = order_value 
        self.time_service = time_service 
        self.time_loading = time_loading 
        self.weight = weight 
        self.customer_id = str(customer_id)
        self.depot_id = str(depot_id)
        self.dx_code = dx_code
        self.state = [depot_id]
        
    
    def update_state(self, current_node_code: str) -> None:
        # print('\tCập nhật trạng thái đơn hàng đã được chuyển tới node có code tương ứng')
        self.state.append(current_node_code)
        return 
    
    def get_current_state(self) -> str:
        '''
        Lấy code của node hiện chứa đơn hàng
        '''
        # print('\tLấy code của node hiện đang chứa đơn hàng')
        return self.state[-1]
    
    def get_path(self):
        if len(self.state) >= 2:
            return self.state[-2] + ' -> ' + self.state[-1]
        else: return self.state[-1]
    def get_start_code(self):
        return self.depot_id
    
    def get_end_code(self):
        return self.customer_id
    
    def get_code(self):
        return self.code

    def print(self) -> None:
        for k, v in self.__dict__.items():
            print(f"{k}: {v}")
        return
    
    
class OrderController:
    def __init__(self, order_dict: dict[str, Order] = None) -> None:
        if order_dict is not None: self.order_dict = order_dict
        self.order_dict: dict[str, Order] = {}
    
    def add(self, order: Order) -> None:
        # print('\tĐã thêm order vào danh sách')
        self.order_dict[order.code] = order
        return
    
    def remove(self, order: Order) -> None:
        print('\tXóa order khỏi danh sách')
        if order.code in self.order_dict.keys():
            del self.order_dict[order.code]
        return
    
    def get_order_dict(self) -> dict[str, Order]:
        return self.order_dict
    
    def get_order_state(self) -> dict[str, str]:
        # print('\tLấy thông tin về code của các node đang cầm các đơn hàng')
        res = {}
        for code, order in self.order_dict.items():
            res[code] = order.get_current_state()
        return res
    
    def get_order_path(self):
        res = {}
        for code, order in self.order_dict.items():
            res[code] = order.get_path()
        return res
    
    def get_order_code(self) -> list[str]:
        return list(self.order_dict.keys())
    
    def length(self) -> int:
        return len(list(self.order_dict.keys()))

    def update_order_state(self, order_code: str, current_node_code: str, remove_flag = False) -> None:
        '''
        Update state của order có code là order_code
        '''
        if order_code not in self.order_dict.keys(): return
        self.order_dict[order_code].update_state(current_node_code)
        if remove_flag: self.order_dict[order_code].state.pop(0)
        return
    
    def get_order(self, order_code) -> Order:
        return self.order_dict[order_code]
    
    def copy(self): 
        res = OrderController()
        for code in self.order_dict:
            res.add(copy.deepcopy(self.order_dict[code]))
        return res

