from hotdata import DataPool
from hotdata.codeInfo import *
import ast
import json
import datetime



def diff(dict1, dict2):
    df = {}
    for key in dict1:
        if key in dict2:
            delta_lines = abs(dict1[key] - dict2[key])
            if delta_lines != 0 :
                df[key] = delta_lines
    print("df :",df)
    return df

def update(old_dict, new_dict):
    for key in new_dict:
        print(key)
        if key not in old_dict:
            
            old_dict[key] = new_dict[key]
        else:
            print("===")
            print(key)
            print("===")
            old_dict[key] += new_dict[key]

def set_code_info_delta(key, data, Pool = DataPool):
    try:
        old_data = get_code_data(key,Pool=DataPool)
    except:
        old_data = {}
    
    df = diff(old_data, data)
    if len(df) != 0:
        now = datetime.datetime.now()
        index = now.hour * 60 + now.minute

        set_active_time(key,index,Pool)
        try:
            old_data_delta = json.loads(Pool.get('user_code_info_delta_%d'%key))
        except:
            old_data_delta = {}
        update(old_data, df)
        old_data = json.dumps(old_data)
        Pool.set('user_code_info_delta_%d'%key, old_data)

    set_code_data(key,data,Pool)



def set_active_time(key, index,Pool=DataPool):
    print(index)
    if not Pool.exists("user_active_time_%d"%key):
        s = " "*200
        Pool.set("user_active_time_%d"%key, s)
    
    Pool.setbit("user_active_time_%d"%key, index, 1)
    


def unit_test():
    set_code_info_delta(1, {'js':1})
    set_code_info_delta(1, {'js':10})
    set_code_info_delta(1, {'js':10, 'c':100})
    set_code_info_delta(1, {'js':10, 'c':100, 'c++':1000})
    print('================')
    print('user_code_info_delta_1')
    print(DataPool.get('user_code_info_delta_%d'%1))
    print('================')
    print('active time :')
    active_time = DataPool.get("user_active_time_%d"%1)
    print(active_time)
    print('================')
    