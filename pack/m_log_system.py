import sys,datetime,json,os

date = datetime.datetime.now().strftime('%Y_%m_%d_%H')
log_output = f'./logs/{date}.txt'

def new_print(*args, **kwargs):
    """
    重写print函数，将输出内容写入日志文件
    """
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = f'🔵 -- {date} --\n'
    for arg in args:
        if arg == 'SYS_ERROR':
            content += f'ERROR '
        else:
            if type(arg) == dict:
                content += "\n{\n"
                for k, v in arg.items():
                    content += f'\t{k}: {v}\n'
                content += "}\n"
            elif type(arg) == list or type(arg) == tuple:
                content += "\n[\n"
                for item in arg:
                    content += f'\t{item}\n'
                content += "]\n"
            else:
                content += f'{arg} '
    print(content)
    with open(log_output, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def clear_log():
    """
    清空日志文件
    """
    for path in os.listdir('/'.join(log_output.split('/')[:-1])):
        if path != log_output.split('/')[-1]:
            os.remove(f'./logs/{path}')
