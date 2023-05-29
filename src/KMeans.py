from BaseClass.Cluster import ClusterController
class KMeans:
    def __init__(self, k) -> None:
        self.k = k
        
    def fit(self) -> ClusterController:
        print('\tThực hiện KMeans và trả về cluster controller chứa thông tin các cụm')
        return ClusterController()