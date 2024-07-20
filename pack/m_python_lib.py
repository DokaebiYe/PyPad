import os, sys
import pkgutil
import inspect,types

def get_all_modules():
    """
    获取当前环境中所有的第三方库和标准库
    """
    modules = sorted([module.name for module in pkgutil.iter_modules()])
    return modules



def get_all_classes(module_name):
    """
    获取指定模块中的所有类
    """
    module = __import__(module_name)
    classes = [module.__dict__[name] for name in dir(module) if isinstance(module.__dict__[name], type)]
    return classes


def get_all_functions(module_name):
    """
    获取指定模块中的所有函数
    """
    try:
        module = __import__(module_name)
        functions = [module.__dict__[name] for name in dir(module) if callable(module.__dict__[name])]
        return functions
    except ImportError:
        print(f"无法导入模块: {module_name}")
        return []

def get_function_params(func):
    """
    获取函数的参数名称和类型
    """
    if not callable(func):
        return None
    if isinstance(func, (types.BuiltinFunctionType, types.BuiltinMethodType)):
        return None  # 跳过内建函数和方法
    try:
        signature = inspect.signature(func)
        params = []
        for name, param in signature.parameters.items():
            param_type = str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any'
            params.append((name, param_type))
        return params
    except (ValueError, TypeError):
        return None  # 跳过无法获取签名的函数


for func in get_all_functions('os'):
    print(func)