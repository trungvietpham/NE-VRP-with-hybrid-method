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
    
def port_order(filename):
    data = pd.read_csv(filename, sep='|')
    customer_id = []
    depot_id = []
    code = []
    for i in range(len(data)):
        line = data.iloc[i]
        if str(line['AcceptancePOSCode']) == 'nan' or str(line['POSCode']) == 'nan': continue
        customer_id.append(str(int(line['AcceptancePOSCode'])))
        depot_id.append(str(int(line['POSCode'])))
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
    
def port_vehicle(filename):
    data = pd.read_csv(filename, sep='|', index_col=False)
    capacity = []
    manager_node = []
    v_type = []
    for i in range(len(data)):
        line = data.iloc[i]
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

if __name__ == '__main__':
    port_order('data_item.csv')