from BaseClass.Node import Node, NodeController
class Cluster:
    ID = 0
    def __init__(self, center) -> None:
        self.center = center
        self.node_child = NodeController()
        self.id = Cluster.ID
        Cluster.ID += 1

    def get_list_node_code(self) -> list:
        print('Lấy thông tin về code của các node nằm trong cluster')
        self.node_child.get_code_list()
        return
    
    def get_center(self) -> list:
        print('Lấy tọa độ tâm')
        return self.center
    
    def add_node(self, node: Node) -> None:
        self.node_child.add(node)
        return
    
class ClusterController:
    def __init__(self) -> None:
        self.cluster_dict = {}
    
    def get_cluster_dict(self) -> dict[int, Cluster]:
        return self.cluster_dict
    
    def add(self, cluster: Cluster):
        self.cluster_dict[cluster.id] = cluster
        return
    
    def remove(self, cluster: Cluster) -> None:
        del self.cluster_dict[cluster.id]
        return
    