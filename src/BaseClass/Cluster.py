class Cluster:
    def __init__(self) -> None:
        pass

    def get_list_node_code(self) -> list:
        print('Lấy thông tin về code của các node nằm trong cluster')
        return
    
    def get_center(self) -> list:
        print('Lấy tọa độ tâm')
        return
    
class ClusterController:
    def __init__(self) -> None:
        self.cluster_dict = {}
    
    def get_cluster_dict(self) -> dict[int, Cluster]:
        return self.cluster_dict
    