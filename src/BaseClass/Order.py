class Order:
    def __init__(self) -> None:
        pass
    
    def update_state(self, current_node_code: str) -> None:
        print('\tCập nhật trạng thái đơn hàng đã được chuyển tới node có code tương ứng')
        return 
    
    def get_current_state(self) -> str:
        '''
        Lấy code của node hiện chứa đơn hàng
        '''
        print('\tLấy code của node hiện đang chứa đơn hàng')
        return
    
    
class OrderController:
    def __init__(self) -> None:
        self.order_dict = {}
    
    def add(self, order: Order):
        print('\tĐã thêm order vào danh sách')
        return
    
    def get_order_dict(self) -> dict[Order]:
        return self.order_dict
    
    def get_order_state(self) -> list:
        print('\tLấy thông tin về code của các node đang cầm các đơn hàng')
        return


