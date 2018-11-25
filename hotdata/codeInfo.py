from hotdata import DataPool
import ast
import json
import datetime

def get_active_time(key, Pool=DataPool):
    '''
        return string in utf-8
    '''
    return Pool.get('user_active_time_%d'%key)

def get_code_delta(key, Pool=DataPool):
    '''
        return json data
    '''
    return Pool.get('user_code_delta_%d'%key)

def get_code_info(key, Pool=DataPool):
    '''
        return json data
    '''
    return Pool.get('user_code_info_%d'%key)



def diff(data1, data2):
    '''
        diff betweew data1 and data2
    '''
    df = {}
    for key in data1: 
        if key not in data2:
            df[key] = data1[key]
        else:
            df[key] = abs(data1[key]-data2[key])

    for key in data2:
        if key not in data1:
            df[key] = data2[key]
        else:
            df[key] = abs(data1[key]-data2[key])
    return df

def update(source, dest):
    '''
        inplace operation 
        update source to dest 
        eg: source = {'js':1 , 'c':1}
            dest = {'c++':20, 'js':2}
            after update dest = {'c++':20, 'js':3, 'c':1}
    '''
    for key in source:
        if key not in dest:
            dest[key] = source[key]
        else:
            dest[key] += source[key]

def process_code_data(key, data, Pool=DataPool):
    old_data = {}
    old = Pool.get('user_code_info_%d'%key)
    if old != None:
        old_data = json.loads(old)
    
    df = diff(old_data, data)

    '''
    ======================
        process code_delta
    '''
    # check if code_delta exists
    code_delta = {}
    delta = Pool.get('user_code_delta_%d'%key)
    if delta != None:
        code_delta = json.loads(delta)

    update(df, code_delta)
    Pool.set('user_code_delta_%d'%key, json.dumps(code_delta))
    '''
        end process code_delta
    =====================
    '''

    '''
    =====================
        process user_active_time 

    '''
    now = datetime.datetime.now()

    index = now.hour*60 + now.minute

    if not Pool.exists('user_active_time_%d'%key):
    
        Pool.set('user_active_time_%d'%key, '\0'*200)

    Pool.setbit('user_active_time_%d'%key, index, 1)


    '''
        end process user_active_time
    =====================
    '''


    Pool.set('user_code_info_%d'%key, json.dumps(data))


'''
=====================================================
unit test
=====================================================
'''


def access_all(key, Pool = DataPool):
    print('user_code_info :', json.loads(Pool.get('user_code_info_%d'%key)) )
    print('user_code_delta :', json.loads(Pool.get('user_code_delta_%d'%key)) )
    print('user_active_time :',Pool.get('user_active_time_%d'%key) )

def test():
    print("="*20, "\ndiff:\n")
    print(diff({'js':100, 'c':101, 'c++':40}, {'ps':100, 'js':100, 'c':102}))
    print('='*20)
    print('='*20, '\nupdate:\n')
    source = {'js':1 , 'c':1}
    dest = {'c++':20, 'js':2}
        
    update(source, dest)
    print('source', source)
    print('dest', dest)
    print('after update operation:', dest)
    print('='*20)
    print('='*20)
    print('process_data:')
    data1 = {'js':100, 'c++':20, 'C#':50}
    data2 = {'c':1, 'js':100}
    data3 = {}
    print('data1: ', data1)
    print('data2: ', data2)
    print('data3: ', data3)
    
    process_code_data(1, data1)
    access_all(1)
    process_code_data(1, data2)
    access_all(1)
    process_code_data(1, data3)
    access_all(1)

