import pandas as pd

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
    for i in range(len(data)):
        # print(i)
        line = data.iloc[i]
        if str(line['Latitude']) == 'nan' or str(line['Longitude']) == 'nan':
            continue
        
        # if(i==9): print(str(line['Longitude']))
        
        lat, lng = float('.'.join(str(line['Latitude']).split(','))), float('.'.join(str(line['Longitude']).split(',')))
        if lat<lng: lat, lng = lng, lat
        id.append(c_id)
        created_at.append('')
        updated_at.append('')
        latitude.append(lat)
        longitude.append(lng)
        address.append(str(line['Address']) + ', '+str(line['districtname'])+', '+str(line['provincename']))
        code.append(line['PoSCode'])
        start_time.append(0)
        end_time.append(60*60*24)
        name.append(str(line['unitname']) + ', ' + str(line['PoSName']))
        tpe.append(line['PoSLevelCode'])
        capacity.append([1e8])
        c_id+=1
    
    save_data = pd.DataFrame(data={'id': id, 'created_at':created_at, 'updated_at': updated_at, 'latitude': latitude, 'longitude': longitude, 
                                   'address':address, 'code': code, 'start_time': start_time, 'end_time': end_time, 
                                   'name': name, 'type': tpe, 'capacity': capacity})
    
    save_data.to_csv('data/node.csv')
    
def port_order(filename, node_fname):
    data = pd.read_csv(filename, sep='|')
    node_data = pd.read_csv(node_fname, sep='|', index_col=False)
    valid_node = node_data['PoSCode'].tolist()
    
    customer_id = []
    depot_id = []
    code = []
    for i in range(len(data)):
        line = data.iloc[i]
        if str(line['AcceptancePOSCode']) == 'nan' or str(line['POSCode']) == 'nan': continue
        if int(line['AcceptancePOSCode']) not in valid_node or int(line['POSCode']) not in valid_node: continue
        depot_id.append(str(int(line['AcceptancePOSCode'])))
        customer_id.append(str(int(line['POSCode'])))
        code.append(line['ItemCode'])
    
    save_data = pd.DataFrame(data={'id': [i+1 for i in range(len(customer_id))], 'created_at': ['' for i in range(len(customer_id))], 
                                   'updated_at': ['' for i in range(len(customer_id))], 'capacity': [1 for i in range(len(customer_id))],
                                   'code': code, 'delivery_after_time': [0 for i in range(len(customer_id))], 'delivery_before_time': [60*60*24 for i in range(len(customer_id))],
                                   'delivery_mode': ['STANDARD' for i in range(len(customer_id))],
                                   'intend_receive_time': ['' for i in range(len(customer_id))],
                                   'order_value': [10000 for i in range(len(customer_id))], 
                                   'time_service': [10 for i in range(len(customer_id))],
                                   'time_loading': [2 for i in range(len(customer_id))],
                                   'weight': [1 for i in range(len(customer_id))], 
                                   'customer_id': customer_id, 'depot_id': depot_id, 'dx_code': ['' for i in range(len(customer_id))]})
    save_data.to_csv('data/order.csv')
    
def port_vehicle(filename, node_fname):
    data = pd.read_csv(filename, sep='|', index_col=False)
    node_data = pd.read_csv(node_fname, sep='|', index_col=False)
    valid_node = node_data['PoSCode'].tolist()
    capacity = []
    manager_node = []
    v_type = []
    for i in range(len(data)):
        line = data.iloc[i]
        if int(line['BuuCuc_QuanLy']) not in valid_node: continue
        
        capacity.append([float(line['TotalLoad'])])
        manager_node.append(int(line['BuuCuc_QuanLy']))
        v_type.append(line['TransportGroupName'])
    
    save_data = pd.DataFrame(data={'id': [i+1 for i in range(len(v_type))], 
                                   'created_at': ['' for i in range(len(v_type))], 
                                   'updated_at': ['' for i in range(len(v_type))],
                                   'available': [1 for i in range(len(v_type))],
                                   'average_fee_transport': [0.1 for i in range(len(v_type))],
                                   'average_gas_consume': [0.02 for i in range(len(v_type))], 
                                   'average_velocity': [60 for i in range(len(v_type))],
                                   'fixed_cost': ['' for i in range(len(v_type))],
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
                                   'dx_code': ['' for i in range(len(v_type))],
                                   'vehicle_cost': ['' for i in range(len(v_type))],
                                   'manager_node': manager_node})
    save_data.to_csv('data/vehicles.csv')

import numpy as np
def distance(point1, point2):
    '''
    Tính khoảng cách l2 giữa 2 điểm tọa độ lat long, trả về khoảng cách km
    '''
    R = 6378.137; # Radius of earth in KM
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
    save_data.to_csv('data/correlations.csv')
        
        
if __name__ == '__main__':
    port_node('buucuc.csv')
    port_vehicle('vehicle.csv', 'buucuc.csv')
    port_order('data_item.csv', 'buucuc.csv')
    port_correlation('correlation.csv', r'data\node.csv')