from BaseClass.Node import Node, NodeController
from BaseClass.Order import OrderController
class Cluster:
    ID = 0
    def __init__(self, center) -> None:
        self.center = center
        self.node_child = NodeController()
        self.id = Cluster.ID
        Cluster.ID += 1

    def get_list_node_code(self) -> list:
        # print('Lấy thông tin về code của các node nằm trong cluster')
        return self.node_child.get_code_list()
        
    
    def get_center(self) -> list:
        # print('Lấy tọa độ tâm')
        return self.center
    
    def add_node(self, node: Node) -> None:
        self.node_child.add(node)
        return
    
    def get_total_weight(self, order_controller: OrderController):
        res = 0
        for code,node in self.node_child.get_node_dict().items():
            res += node.get_total_weight(order_controller)
        return res
            
    def print(self):
        print(self.node_child.get_code_list())
    
class ClusterController:
    def __init__(self) -> None:
        self.cluster_dict: dict[int, Cluster] = {}
    
    def get_cluster_dict(self) -> dict[int, Cluster]:
        return self.cluster_dict
    
    def add(self, cluster: Cluster):
        self.cluster_dict[cluster.id] = cluster
        return
    
    def remove(self, cluster: Cluster) -> None:
        del self.cluster_dict[cluster.id]
        return
    
    def to_json(self, filename): 
        clusters = {}
        for i in range(len(self.cluster_dict)):
            clusters[i] = {}
            clusters[i]['ID'] = self.cluster_dict[i].ID
            clusters[i]['center'] = self.cluster_dict[i].center
            # clusters[i]['n_childrens'] = self.cluster_dict[i].
            