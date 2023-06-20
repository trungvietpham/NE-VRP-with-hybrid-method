class Vehicle:
    def __init__(self, 
                 id, 
                 created_at, 
                 updated_at, 
                 available, 
                 average_fee_transport, 
                 average_gas_consume, 
                 average_velocity, 
                 fixed_cost, 
                 driver_name, 
                 gas_price, 
                 height, 
                 length, 
                 max_capacity, 
                 max_load_weight, 
                 max_velocity, 
                 min_velocity, 
                 name, 
                 type, 
                 width, 
                 dx_code, 
                 vehicle_cost,
                 manager_node,
                 current_node: str = None) -> None:
        '''
        manager_node: code của manager node
        '''
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.available = available
        self.average_fee_transport = average_fee_transport
        self.average_gas_consume = average_gas_consume
        self.average_velocity = average_velocity
        self.fixed_cost = fixed_cost
        self.driver_name = driver_name
        self.gas_price = gas_price
        self.height = height
        self.length = length
        self.max_capacity = max_capacity
        self.max_load_weight = max_load_weight
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.name = name
        self.type = type
        self.width = width
        self.dx_code = dx_code
        self.vehicle_cost = vehicle_cost
        self.manager_node = manager_node
        self.current_node = current_node
        return
    
    def update_current_node(self, current_node: str):
        self.current_node = current_node
        return
    
    def print(self) -> None:
        for item in self.__dict__.items():
            print(f"{item[0]}: {item[1]}")

class VehicleController:
    def __init__(self) -> None:
        self.vehicle_dict: dict[str, Vehicle] = {}

    def add(self, vehicle: Vehicle) -> None:
        # print('Thêm vehicle vào vehicleController')
        self.vehicle_dict[vehicle.id] = vehicle
        return
    
    def remove(self, vehicle: Vehicle) -> None:
        # print('Xóa vehicle khỏi dict')
        if vehicle.id in self.vehicle_dict.keys():
            del self.vehicle_dict[vehicle.id]
        return
    
    def get_vehicle(self, id: int) -> Vehicle:
        if id in self.vehicle_dict.keys():
            return self.vehicle_dict[id]
        else: return None
    
    def get_vehicle_dict(self) -> dict[int, Vehicle]:
        return self.vehicle_dict
    
    def update_vehicle_state(self, v_code, current_state):
        if v_code in self.vehicle_dict:
            self.vehicle_dict[v_code].update_current_node(current_state)
        return
    
    def print(self):
        for code in self.vehicle_dict:
            print(self.vehicle_dict[code].max_capacity)
            input('Stop')
