class Correlation:
    def __init__(self, id, 
                 created_at, 
                 updated_at, 
                 distance, 
                 from_node_code, 
                 from_node_id, 
                 from_node_name, 
                 from_node_type, 
                 risk_probability, 
                 time, to_node_code, 
                 to_node_id, 
                 to_node_name, 
                 to_node_type) -> None:
        self.created_at = created_at 
        self.updated_at = updated_at 
        self.distance = float(distance)
        self.from_node_code = str(int(from_node_code))
        self.from_node_id = from_node_id
        self.from_node_name = str(from_node_name)
        self.from_node_type = from_node_type
        self.risk_probability = risk_probability
        self.time = time
        self.to_node_code = str(int(to_node_code)) 
        self.to_node_id = to_node_id
        self.to_node_name = str(to_node_name)
        self.to_node_type = to_node_type
        
    def print(self) -> None:
        for k, v in self.__dict__.items():
            print(f"{k}: {v}")
        return
    

class CorrelationController:
    def __init__(self) -> None:
        self.correlation_dict: dict[str, Correlation] = {}
        return 
    
    def add(self, correlation: Correlation) -> None: 
        # print(f'Add {str(correlation.from_node_code)} - {str(correlation.to_node_code)}')
        # input('Add')
        self.correlation_dict[str(correlation.from_node_code)+ '-'+str(correlation.to_node_code)] = correlation
        return
    
    def remove(self, correlation: Correlation) -> None: 
        if (str(correlation.from_node_code) + '-' + str(correlation.to_node_code)) in self.correlation_dict.keys():
            del self.correlation_dict[str(correlation.from_node_code) + '-' + str(correlation.to_node_code)]
        return
    
    def get_correlation_dict(self) -> dict[str, Correlation]: 
        return self.correlation_dict
    
    def get_correlation(self, start_code, end_code) -> Correlation:
        # print(f"{start_code}, {end_code}")
        id = str(start_code) + '-' + str(end_code)
        # print(f"ID: {id}")
        # input('ID')
        if id in self.correlation_dict:
            # print(f"Found correlation = {self.correlation_dict[id]}")
            # input('Corr: ')
            return self.correlation_dict[id]
        return None