import os


storge_path = f'./cache'


def save_data(key,data):
    """
    保存数据到本地
    """
    with open(f'{storge_path}/{key}.dat', 'w',encoding='utf-8') as f:
        f.write(data)

def read_data(key):
    """
    读取本地数据
    """
    with open(f'{storge_path}/{key}.dat', 'r',encoding='utf-8') as f:
        data = f.read()
    return data

def remove_data(key):
    """
    删除本地数据
    """
    try:
        os.remove(f'{storge_path}/{key}.dat')
    except:
        pass