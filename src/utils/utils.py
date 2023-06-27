import random
import pandas as pd
import os
import sys
sys.path.append('..')

def port_node(filename):
    # f = open(filename, 'r') 
    id = []
    created_at = []
    updated_at = []
    latitude = []
    longitude = []
    address = []
    code = []
    start_time = []
    end_time = []
    name = []
    tpe = []
    capacity = []
    
    c_id = 0
    data = pd.read_csv(filename, sep='|', index_col=False)
    # print(len(data))
    # input()
    for i in range(len(data)):
        # print(i)
        line = data.iloc[i]
        # print(line)
        # input('Stop')
        # if str(line['Latitude']) == 'nan' or str(line['Longitude']) == 'nan':
        #     continue
        
        # if(i==9): print(str(line['Longitude']))
        
        lat, lng = float('.'.join(str(line['Latitude']).split(','))), float('.'.join(str(line['Longitude']).split(',')))
        if lat>lng: lat, lng = lng, lat
        id.append(c_id)
        created_at.append('2023-06-18 16:37:06')
        updated_at.append('2023-06-18 16:37:06')
        latitude.append(lat)
        longitude.append(lng)
        address.append(str(line['Address']) + ', '+str(line['districtname'])+', '+str(line['provincename']))
        code.append(line['PoSCode'])
        rand = random.randint(0,1)
        start_time.append(rand * 60*60*24/2)
        end_time.append((rand+1)*60*60*24/2)
        name.append(str(line['unitname']) + ', ' + str(line['PoSName']))
        tpe.append(line['PoSLevelCode'])
        capacity.append(1e8)
        c_id+=1
    print(f"{len(latitude)}, {len(longitude)}, {len(id)}, {len(created_at), len(updated_at), len(address), len(code), len(start_time), len(end_time), len(name), len(tpe), len(capacity), len(data['ProvinceCode'].tolist())}")
    save_data = pd.DataFrame(data={'created_at':created_at, 'updated_at': updated_at, 'code': code, 'latitude': latitude, 'longitude': longitude, 
                                   'address':address, 'start_time': start_time, 'end_time': end_time, 
                                   'name': name, 'type': tpe, 'capacity': capacity, 'province_code': data['ProvinceCode'].tolist(), 
                                   'district_code': data['DistrictCode'].tolist()})
    save_data.to_csv('data/node.tsv', sep='\t', index=False)
    
def port_order(filename, node_fname):
    data = pd.read_csv(filename, sep='|')
    node_data = pd.read_csv(node_fname, sep='|', index_col=False)
    valid_node = node_data['PoSCode'].tolist()
    
    customer_id = []
    depot_id = []
    code = []
    weight = []
    for i in range(len(data)):
        line = data.iloc[i]
        if str(line['AcceptancePOSCode']) == 'nan' or str(line['POSCode']) == 'nan': continue
        if int(line['AcceptancePOSCode']) not in valid_node or int(line['POSCode']) not in valid_node: continue
        depot_id.append(str(int(line['AcceptancePOSCode'])))
        customer_id.append(str(int(line['POSCode'])))
        code.append(line['ItemCode'])
        weight.append(float(line['Weight']) / 1e3)
    
    save_data = pd.DataFrame(data={'code': code, 
                                   'created_at': ['2023-06-18 16:37:06' for i in range(len(customer_id))], 
                                   'updated_at': ['2023-06-18 16:37:06' for i in range(len(customer_id))], 
                                   'capacity': [1 for i in range(len(customer_id))],
                                   'delivery_after_time': [0 for i in range(len(customer_id))], 
                                   'delivery_before_time': [60*60*24 for i in range(len(customer_id))],
                                   'delivery_mode': ['STANDARD' for i in range(len(customer_id))],
                                   'order_value': [10000 for i in range(len(customer_id))], 
                                   'time_service': [10 for i in range(len(customer_id))],
                                   'time_loading': [2 for i in range(len(customer_id))],
                                   'weight': weight, 
                                   'receiver_code': customer_id, 'sender_code': depot_id})
    save_data.to_csv('data/order.tsv', sep='\t', index=False)
    
def port_vehicle(filename, node_fname):
    data = pd.read_csv(filename, sep='|', index_col=False)
    node_data = pd.read_csv(node_fname, sep='|', index_col=False)
    valid_node = node_data['PoSCode'].tolist()
    # print(valid_node)
    # input('ashdue')
    capacity = []
    manager_node = []
    v_type = []
    check = {}
    for i in range(len(data)):
        line = data.iloc[i]
        m_node = int(line['BuuCuc_QuanLy'])
        
        if m_node not in valid_node:
            if m_node % 100 == 0: 
                if (m_node - 100) in valid_node: 
                    m_node = m_node-100
                    # print('Found 1')
                else: continue
            
            elif m_node%10 == 0:
                if (m_node-10) in valid_node: 
                    # print('Found 2')
                    m_node = m_node-10
                else: continue
            else: continue
        if m_node not in check: check[m_node] = 0
        if check[m_node] >= 10: continue
        check[m_node] += 1
        
        load = float(line['TotalLoad'])*1000
        while load>15000:
            load = load//10
        load = int(load)
        capacity.append(load)
        manager_node.append(m_node)
        v_type.append(line['TransportGroupName'])
        
        if check[m_node] == 1:
            capacity.append(random.randint(20000, 30000))
            manager_node.append(m_node)
            v_type.append(line['TransportGroupName'])
    
    save_data = pd.DataFrame(data={'code': [i+1 for i in range(len(v_type))], 
                                   'created_at': ['2023-06-21 11:28:20' for i in range(len(v_type))], 
                                   'updated_at': ['2023-06-21 11:28:20' for i in range(len(v_type))],
                                   'available': [1 for i in range(len(v_type))],
                                   'average_fee_transport': [0.1 for i in range(len(v_type))],
                                   'average_gas_consume': [0.02 for i in range(len(v_type))], 
                                   'average_velocity': [60 for i in range(len(v_type))],
                                   'driver_name': ['' for i in range(len(v_type))],
                                   'gas_price': [22000 for i in range(len(v_type))],
                                   'height': ['' for i in range(len(v_type))],
                                   'length': ['' for i in range(len(v_type))],
                                   'max_capacity': capacity,
                                   'max_load_weight': ['' for i in range(len(v_type))],
                                   'max_velocity': [90 for i in range(len(v_type))],
                                   'min_velocity': [40 for i in range(len(v_type))],
                                   'name': ['' for i in range(len(v_type))],
                                   'type': v_type,
                                   'width': ['' for i in range(len(v_type))],
                                   'vehicle_cost': ['' for i in range(len(v_type))],
                                   'manager_node': manager_node, 
                                   'current_node': manager_node})
    save_data.to_csv('data/vehicles.tsv', sep='\t', index=False)

import numpy as np
def distance(point1, point2):
    '''
    Tính khoảng cách l2 giữa 2 điểm tọa độ lat long, trả về khoảng cách km
    '''
    R = 6371.137; # Radius of earth in KM
    dLat = (point2[0] - point1[0])*np.pi/180
    dLon = (point2[1]-point1[1])*np.pi/180
    a = np.sin(dLat/2) ** 2 + np.cos(point1[0]*np.pi/180) * np.cos(point2[0]* np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R*c
    return d

def port_correlation(filename, node_fname):
    data = pd.read_csv(filename, sep='|', index_col=False)
    node_data = pd.read_csv(node_fname, sep=',', index_col=False)
    valid_node = {}
    for i in range(len(node_data)):
        line = node_data.iloc[i]
        if line['code'] in valid_node: continue
        valid_node[line['code']] = [line['latitude'], line['longitude']]
    # valid_node = node_data['code'].tolist()
    from_node_code = []
    to_node_code = []
    dis = []
    check = {}
    for i in range(len(data)):
        line = data.iloc[i]
        if line['send'] not in valid_node or line['receive'] not in valid_node: continue
        # print(str(line['send']) + ','+str(line['receive']))
        if (str(line['send']) + ','+str(line['receive'])) in check:
            continue
        lldis = distance(valid_node[line['send']], valid_node[line['receive']])
        from_node_code.append(line['send'])
        to_node_code.append(line['receive'])
        dis.append(lldis)
        from_node_code.append(line['receive'])
        to_node_code.append(line['send'])
        dis.append(lldis)
        check[str(line['send']) + ','+str(line['receive'])] = 1
        check[str(line['send']) + ','+str(line['receive'])] = 1
    save_data = pd.DataFrame(data = {'id': [i+1 for i in range(len(dis))], 
                                     'created_at': ['' for i in range(len(dis))], 
                                     'updated_at': ['' for i in range(len(dis))],
                                     'distance': dis,
                                     'from_node_code': from_node_code,
                                     'from_node_id': ['' for i in range(len(dis))],
                                     'from_node_name': ['' for i in range(len(dis))],
                                     'from_node_type': ['' for i in range(len(dis))], 
                                     'risk_probability': ['' for i in range(len(dis))], 
                                     'time': ['' for i in range(len(dis))], 
                                     'to_node_code': to_node_code,
                                     'to_node_id': ['' for i in range(len(dis))],
                                     'to_node_name': ['' for i in range(len(dis))],
                                     'to_node_type': ['' for i in range(len(dis))]})
    save_data.to_csv('data/correlations.tsv', sep='\t', index=False)
        
def port_correlation2(filename, node_fname):
    node_data = pd.read_csv(node_fname, sep='\t', index_col=False)
    from_node_code = []
    to_node_code = []
    from_node_type = []
    to_node_type = []
    dis = []
    epsilon = 10
    for i in range(len(node_data)): 
        print(f'i = {i}')
        line_i = node_data.iloc[i]
        for j in range(i, len(node_data)):
            line_j = node_data.iloc[j]
            flag = 0
            if line_i['type'] == line_j['type'] and line_j['type'] == 'GD1': flag = 1
            elif line_i['province_code'] == line_j['province_code']:
                # if (line_i['type'] == 'GD1' or line_i['type'] == 'GD2') and (line_j['type'] == 'GD1' or line_j['type'] == 'GD2'): flag = 1
                # elif ((line_i['type'] == 'GD2' or line_i['type'] == 'GD3') and (line_j['type'] == 'GD3' or line_j['type'] == 'GD2')) and \
                #     line_i['district_code'] == line_j['district_code']: flag = 1
                # elif distance([line_i['latitude'], line_i['longitude']], [line_j['latitude'], line_j['longitude']]) < epsilon: flag = 1
                if line_i['type'] in ['GD1', 'GD2', 'GD3'] and line_j['type'] in ['GD1', 'GD2', 'GD3']: flag = 1
            if flag == 1:
                lldis = distance([line_i['latitude'], line_i['longitude']], [line_j['latitude'], line_j['longitude']])
                from_node_code.append(line_i['code'])
                to_node_code.append(line_j['code'])
                from_node_type.append(line_i['type'])
                to_node_type.append(line_j['type'])
                dis.append(lldis)
                from_node_code.append(line_j['code'])
                to_node_code.append(line_i['code'])
                from_node_type.append(line_j['type'])
                to_node_type.append(line_i['type'])
                dis.append(lldis)
    save_data = pd.DataFrame(data = {'id': [i+1 for i in range(len(dis))], 
                                     'created_at': ['' for i in range(len(dis))], 
                                     'updated_at': ['' for i in range(len(dis))],
                                     'distance': dis,
                                     'from_node_code': from_node_code,
                                     'from_node_id': ['' for i in range(len(dis))],
                                     'from_node_name': ['' for i in range(len(dis))],
                                     'from_node_type': from_node_type, 
                                     'risk_probability': ['' for i in range(len(dis))], 
                                     'time': ['' for i in range(len(dis))], 
                                     'to_node_code': to_node_code,
                                     'to_node_id': ['' for i in range(len(dis))],
                                     'to_node_name': ['' for i in range(len(dis))],
                                     'to_node_type': to_node_type})
    save_data.to_csv('data/correlations.tsv', sep='\t', index=False)

if __name__ == '__main__':
    print(os.getcwd())
    # port_node(r'tmp\buucuc.csv')
    port_vehicle('vehicle.csv', r'tmp\buucuc.csv')
    # port_order('data_item.csv', r'tmp\buucuc.csv')
    # port_correlation2('correlation.csv', r'data\node.tsv')
    
    # print(distance([21.02616843,105.8535759], [21.153,105.4954]))