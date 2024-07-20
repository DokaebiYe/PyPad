import os,sys

def get_all_folders(path):
    """
    获取指定目录下的所有文件夹
    """
    folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    return folders

def get_all_files(path):
    """
    获取指定目录下的所有文件
    """
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    return files

def get_structure(path):
    """
    获取指定目录下的所有文件夹和文件
    """
    folders = get_all_folders(path)
    files = get_all_files(path)
    return folders, files

def get_name(path):
    """
    获取指定路径的文件或文件夹名称
    """
    return os.path.basename(path)

def get_parent(path):
    """
    获取指定路径的父目录
    """
    return os.path.dirname(path)

# 操作

def create_folder(path):
    """
    创建一个文件夹
    """
    os.makedirs(path, exist_ok=True)

def remove_folder(path):
    """
    删除一个文件夹, 包括其中的所有文件和文件夹
    """
    try:
        os.removedirs(path)
    except:
        pass

def remove_folder_content(path):
    """
    删除一个文件夹中的所有文件和文件夹
    """
    for folder in get_all_folders(path):
        remove_folder(os.path.join(path, folder))
    for file in get_all_files(path):
        remove_file(os.path.join(path, file))

def create_file(path):
    """
    创建一个文件
    """
    with open(path, 'w',encoding='utf-8') as f:
        pass

def remove_file(path):
    """
    删除一个文件
    """
    try:
        os.remove(path)
    except:
        pass

def copy_file(src, dst):
    """
    复制一个文件
    """
    with open(src, 'rb',encoding='utf-8') as f:
        content = f.read()
    with open(dst, 'wb',encoding='utf-8') as f:
        f.write(content)

def move_file(src, dst):
    """
    移动一个文件, 如果dst已存在, 则覆盖
    """
    copy_file(src, dst)
    remove_file(src)

def move_folder(src, dst):
    """
    移动一个文件夹, 如果dst已存在, 则覆盖
    """
    try:
        os.rename(src, dst)
    except:
        pass

def read_file(path):
    """
    读取一个文件的内容
    """
    with open(path, 'r',encoding='utf-8') as f:
        content = f.read()
    return content

def write_file(path, content):
    """
    写入内容到一个文件
    """
    with open(path, 'w',encoding='utf-8') as f:
        f.write(content)

def append_file(path, content):
    """
    追加内容到一个文件
    """
    with open(path, 'a',encoding='utf-8') as f:
        f.write(content)
