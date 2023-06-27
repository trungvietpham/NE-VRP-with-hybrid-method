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
            route = self.main_order.get_order(code).state + self.support_order.get_order(code).state[::-1][1:]
            transit_vehicle = self.main_order.get_order(code).transit_vehicle + self.support_order.get_order(code).transit_vehicle[::-1]
            # print(transit_vehicle)
            # input('1q223r')
            # print(type(code))
            # input('ashue')
            res[code] = [route, transit_vehicle]
            # for i in range(1, len(route)):
            #     res[code].append([route[i], transit_vehicle[i-1]])
        return res
    
    def get_vehicle_route(self):
        folder = 'scenarios/'
        sender = json.load(open(folder+'output_sender_side.GD2-GD1.json', 'r'))
        receiver = json.load(open(folder+'output_receiver_side.GD2-GD1.json', 'r'))
        sender_receiver = json.load(open(folder+'output_sender_receiver.GD1-GD1.json', 'r'))
        res = {}
        for code in sender['vehicle']: 
            if code not in res: res[code] = []
            a_dict = {'start_node': [], 'end_node': [], 'order': [], 'type': [], 'phase': []}
            for i in range(len(sender['vehicle'][code]) - 1):
                a_dict['start_node'].append(sender['vehicle'][code][i])
                a_dict['end_node'].append(sender['vehicle'][code][i+1])
                if i == 0: a_dict['order'].append([])
                else: 
                    if a_dict['start_node'][-1] in sender['node']:
                        o = list(set(sender['node'][a_dict['start_node'][-1]]))
                    else: o = []
                    a_dict['order'].append(o)
                a_dict['type'].append('pickup')
                a_dict['phase'].append('1')
                
            res[code].append(a_dict)
        
        # return res
        order_des = {}
        for order, node in sender_receiver['order'].items():
            node = node.split(' -> ')[1]
            if node not in order_des: order_des[node] = []
            order_des[node].append(order)
            
        for code in sender_receiver['vehicle']:
            if code not in res: res[code] = []
            a_dict = {'start_node': [], 'end_node': [], 'order': [], 'type': [], 'phase': []}
            for i in range(len(sender_receiver['vehicle'][code])-1): 
                a_dict['start_node'].append(sender_receiver['vehicle'][code][i])
                a_dict['end_node'].append(sender_receiver['vehicle'][code][i+1])
                # if i == 0: 
                #     a_dict['order'].append(sender_receiver['node'][sender['vehicle'][code][i]])
                #     a_dict['type'].append('pickup')
                # else: 
                a_dict['order'].append(order_des[a_dict['end_node'][-1]])
                a_dict['type'].append('delivery')
                a_dict['phase'].append('2')
            res[code].append(a_dict)
            
        order_des = {}
        for order, node in receiver['order'].items():
            node = node.split(' -> ')
            if len(node) != 2: continue
            node = node[0]
            if node not in order_des: order_des[node] = []
            order_des[node].append(order)
        
        for code in receiver['vehicle']:
            if code not in res: res[code] = []
            a_dict = {'start_node': [], 'end_node': [], 'order': [], 'type': [], 'phase': []}
            for i in range(len(receiver['vehicle'][code])-2): 
                a_dict['start_node'].append(receiver['vehicle'][code][i])
                a_dict['end_node'].append(receiver['vehicle'][code][i+1])
                # if i == 0: 
                #     a_dict['order'].append(receiver['node'][sender['vehicle'][code][i]])
                #     a_dict['type'].append('pickup')
                # else: 
                a_dict['order'].append(order_des[a_dict['end_node'][-1]])
                a_dict['type'].append('delivery')
                a_dict['phase'].append('3')
            res[code].append(a_dict)
            
        return res

                
            
    def output_to_file(self, data, filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename)) 
        json.dump(data, open(filename, 'w'), indent=4)
    
    # def visualize(self)
    def execute(self, output_filename):
        pass        