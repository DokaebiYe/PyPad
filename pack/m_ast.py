import ast,types,inspect,os,sys


def new_class(name):
    """
    创建一个新的类，返回AST节点
    """
    return ast.ClassDef(
        name=name,
        bases=[],
        keywords=[],
        body=[],
        decorator_list=[],
    )

def new_function(name):
    """
    创建一个新的函数，返回AST节点
    """
    return ast.FunctionDef(
        name=name,
        args=ast.arguments(
            args=[],
            posonlyargs=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=[],
        decorator_list=[],
    )

def new_expression(expression):
    """
    创建一个新的表达式，返回AST节点
    """
    return ast.Expr(
        value=expression,
    )

def new_import(module):
    """
    创建一个新的导入语句，返回AST节点
    """
    return ast.Import(
        names=[ast.alias(name=module, asname=None)],
    )

def new_import_from(module, names):
    """
    创建一个新的从模块中导入的语句，返回AST节点
    """
    return ast.ImportFrom(
        module=module,
        names=[ast.alias(name=name, asname=None) for name in names],
        level=0,
    )

def new_assign(target, value):
    """
    创建一个新的赋值语句，返回AST节点
    """
    return ast.Assign(
        targets=[target],
        value=value,
    )

def new_return(value):
    """
    创建一个新的返回语句，返回AST节点
    """
    return ast.Return(
        value=value,
    )

def new_call(func, args):
    """
    创建一个新的函数调用，返回AST节点
    """
    return ast.Call(
        func=func,
        args=args,
        keywords=[],
    )

def add_to_node(node, item):
    """
    向AST节点中添加一个子节点
    """
    node.body.append(item)

def add_function_args(func, args):
    """
    向函数中添加参数
    """
    func.args.args = args

def add_class_body(cls, item):
    """
    向类中添加方法
    """
    cls.body.append(item)

def empty_file():
    """
    创建一个空的Python文件
    """
    return ast.Module(
        body=[],
    )