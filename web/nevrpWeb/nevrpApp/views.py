import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import os


import pandas as pd
def get_node_loation():
    data = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'node.tsv'), sep='\t')
    res = {}
    for i in range(len(data)):
        line = data.iloc[i]
        res[str(line['code'])] = f"{float(line['latitude'])},{str(line['longitude'])}"
    return res
def get_address(): 
    data = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'node.tsv'), sep='\t')
    res = {}
    for i in range(len(data)):
        line = data.iloc[i]
        res[str(line['code'])] = f"{line['address']}"
    return res

location_map = get_node_loation()
address_map = get_address()
# Create your views here.

def home(request):
    context = {}
    return render(request, "nevrpApp/home.html", context)

def order(request):
    order = Order.objects.all()
    concept = {'order': []}
    for k in range(len(order)):
        o = order.__getitem__(k)
        # print(o.sender_code)
        concept['order'].append({'code': str(o.code), 'sender_code': address_map[str(o.sender_code)], 'receiver_code': address_map[str(o.receiver_code)], 'delivery_mode': str(o.delivery_mode)})
        # print(order.__getitem__(k).code)
    return render(request, "nevrpApp/order.html", concept)

def node(request):
    node = Node.objects.all()
    return render(request, 'nevrpApp/node.html', {'node': node})

def vehicle(request):
    vehicle = Vehicle.objects.all()
    return render(request, 'nevrpApp/vehicle.html', {'vehicle': vehicle})

def order_result(request):
    data = Order.objects.values_list('code', flat=True)
    return render(request, 'nevrpApp/order_result.html', {'order_result': data})

def node_result(request):
    data = Node.objects.values_list('code', flat=True)
    return render(request, 'nevrpApp/node_result.html', {'node_result': data})

def vehicle_result(request):
    data = Vehicle.objects.values_list('code', flat=True)
    # print(list(data))
    return render(request, 'nevrpApp/vehicle_result.html', {'vehicle_result': data})

def search_vehicle(request):
    print(os.getcwd())
    path = os.path.join(os.getcwd(), '..', '..', 'scenarios')
    data = json.load(open(path + "/vehicle.json")) # Read from file
    # location_map = get_node_loation()
    # address_map = get_address()
    code = request.POST['code']
    print(code)
    # print(data)
    concept = []
    if code not in data: return render(request, 'nevrpApp/vehicle_result.html', {}) 
    print('Yes')
    vehicle_route = data[code]
    # print(order_path)
    gmap_header = 'https://www.google.com/maps/dir/'
    for i in range(len(vehicle_route)):
        route_data = vehicle_route[i]
        point_for_map = []
        for j in range(len(route_data['start_node'])):
            
            if j==0: r_n = i+1
            else: r_n = ''
            location_map[route_data['end_node'][j]]
            if j==0:
                point_for_map.append(location_map[route_data['start_node'][j]])
            point_for_map.append(location_map[route_data['end_node'][j]])
            # print(point_for_map)
            if j == len(route_data['start_node']) - 1: 
                gmap_body = '/'.join(point_for_map)
            else: gmap_body = f"{point_for_map[j]}/{point_for_map[j+1]}"
            
            concept.append({'routes_number': r_n, 'start_node': address_map[route_data['start_node'][j]] + f" ({str(route_data['start_node'][j])})", 'end_node': address_map[route_data['end_node'][j]] + f" ({str(route_data['end_node'][j])})", 'order': ', '.join(route_data['order'][j]), 'type': route_data['type'][j], 'phase': route_data['phase'][j], 'view_in_maps': gmap_header+gmap_body})
    # print(concept)
    return render(request, 'nevrpApp/vehicle_result.html', {"res": concept})

def search_order(request):
    path = os.path.join(os.getcwd(), '..', '..', 'scenarios')
    data = json.load(open(path + "/order.json")) # Read from file
    code = request.POST['code']
    print(code)
    # print(data)
    concept = []
    if str(code) not in data: return render(request, 'nevrpApp/order_result.html', {}) 
    print('Yes')
    order_path = data[code]
    # print(order_path)
    for i in range(len(order_path[0]) - 1):
        concept.append({'code': code, 'start_node': address_map[str(order_path[0][i])] + f" ({str(order_path[0][i])})", 'end_node': address_map[str(order_path[0][i+1])] + f" ({str(order_path[0][i+1])})", 'transit_vehicle': order_path[1][i]})
    print(concept)
    return render(request, 'nevrpApp/order_result.html', {'res': concept})