import json
import os
import plotly as plt
import numpy as np
from BaseClass.Node import NodeController
from BaseClass.Order import OrderController
class Visualize:
    def __init__(self, all_node_hierarchacal: dict[str, NodeController], main_order: OrderController, support_order: OrderController) -> None:
        self.all_node = all_node_hierarchacal
        self.main_order = main_order
        self.support_order = support_order
    
    def get_node_code_hierarchacal(self) -> dict[str, list[str]]:
        res = {}
        for e in self.all_node:
            res[e] = self.all_node[e].get_code_list()
        return res
    
    def get_node_location_hierarchacal(self) -> dict[str, np.ndarray]:
        res: dict[str, np.ndarray|list] = {}
        for e in self.all_node:
            res[e] = []
            for node in list(self.all_node[e].get_node_dict().values()):
                res[e].append(node.get_location())
            res[e] = np.array(res[e])
        return res
    
    def get_order_route(self) -> dict[str, list]:
        res = {}
        for code in self.main_order.get_order_dict():
            # print(f"{self.main_order.get_order(code).state}, {self.support_order.get_order(code).state[::-1][:-1]}")
            # input('Order rtoute')
            res[code] = self.main_order.get_order(code).state + self.support_order.get_order(code).state[::-1][:-1]
        return res
    
    def output_order(self, data, filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename)) 
        json.dump(data, open(filename, 'w'), indent=4)
    
    # def visualize(self)
    def execute(self, output_filename):
        pass        