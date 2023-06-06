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
        self.delivery_after_time = delivery_after_time
        self.delivery_before_time = delivery_before_time
        self.delivery_mode = delivery_mode 
        self.intend_receive_time = intend_receive_time 
        self.order_value = order_value 
        self.time_service = time_service 
        self.time_loading = time_loading 
        self.weight = weight 
        self.customer_id = customer_id 
        self.depot_id = depot_id
        self.dx_code = dx_code
        self.state = [depot_id]
        
    
    def update_state(self, current_node_code: str) -> None:
        print('\tCập nhật trạng thái đơn hàng đã được chuyển tới node có code tương ứng')
        self.state.append(current_node_code)
        return 
    
    def get_current_state(self) -> str:
        '''
        Lấy code của node hiện chứa đơn hàng
        '''
        print('\tLấy code của node hiện đang chứa đơn hàng')
        return self.state[-1]

    def print(self) -> None:
        for k, v in self.__dict__.items():
            print(f"{k}: {v}")
        return
    
    
class OrderController:
    def __init__(self) -> None:
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
    
    def get_order_state(self) -> list:
        print('\tLấy thông tin về code của các node đang cầm các đơn hàng')
        res = []
        for order in list(self.order_dict.values()):
            res.append(order.get_current_state())
        return res


