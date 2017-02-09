#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Make inspect easier
  Created: 2017/1/2
"""

import unittest
import inspect
import types
from types import FunctionType
from types import MethodType
from pprint import pprint
#import ip_calc_utils 

#----------------------------------------------------------------------
def get_callables(module_or_instance):
    """Get all callable mamber from [module_or_instance]
    
    Params:
        module_or_instance: :str: the name of module or instance
    
    Returns:
        A list stored the callable objects"""
    result = []
    
    for i in inspect.getmembers(module_or_instance):
        if callable(i[1]):
            result.append(i[1])
        else:
            pass
        
    return result

#----------------------------------------------------------------------
def get_fileds(module_or_instance, type=None, public=True):
    """Get all field member from [module_or_instance]
    
    Params:
        module_or_instance: :str: the name of module or instance
        type: :type: the type you want to filter or tuple([type1, type2])
        pubic: :bool: do you want to inspect all field?
        
    Returns:
        A dict stored the keys and values."""
    result = {}
    
    for i in inspect.getmembers(module_or_instance):
        if not callable(i[1]):
            if i[0].startswith('_') and public:
                pass
            else:
                if type != None:
                    if isinstance(i[1], type):
                        result[i[0]] = i[1]
                    else:
                        pass
                else:
                    result[i[0]] = i[1]
        else:
            pass
        
    return result

#----------------------------------------------------------------------
def get_functions(module_or_instance, public=True):
    """Get all function from [module_or_instance]
    
    Params:
        module_or_instance: :str: the name of module or instances
        public: :bool: get the public function?
            'public' means that the [name].startswith('_') is true.
    
    Returns:
        A list stored the function from module/instance
    """
    ret = []
    
    for i in get_callables(module_or_instance):
        if isinstance(i, FunctionType):
            ret.append(i)
    
    if public:
        for i in range(len(ret)):
            if ret[i].__name__.startswith('_'):
                ret[i] = None
        while True:
            try:
                ret.remove(None)
            except ValueError:
                break
    else:
        pass
    
    while True:
        try:
            ret.remove(None)
        except ValueError:
            break
        
    return ret

#----------------------------------------------------------------------
def get_methods(instance, public=True):
    """Get methods from instance"""
    
    ret = []
    
    for i in get_callables(instance):
        if isinstance(i, MethodType):
            ret.append(i)
    
    if public:
        for i in range(len(ret)):
            if ret[i].__name__.startswith('_'):
                ret[i] = None
        while True:
            try:
                ret.remove(None)
            except ValueError:
                break
    else:
        pass
    
    while True:
        try:
            ret.remove(None)
        except ValueError:
            break
        
    return ret    

#----------------------------------------------------------------------
def get_args_dict(func):
    """"""
    assert callable(func), '[!] The [func] you input cannot be called!'
    
    result = {}
    
    try:
        func_name = getattr(func, '__name__')
    except:
        func_name = str(func)
    
    #
    # Process args
    #
    args = {}
    spec = inspect.getargspec(func)
    args['vargs'] = spec.varargs
    args['kwargs'] = spec.keywords
    args['defaults'] = spec.defaults if spec.defaults else []
    args['args'] = spec.args
    args['args_table'] = {}
    
    for i in spec.args:
        args['args_table'][i] = None
    
    for i in range(len(args['defaults'])):
        index = -1 - i
        args['args_table'][spec.args[index]] = spec.defaults[index]
    
    result['func_name'] = func_name
    result['args'] = args
    
    return result

#----------------------------------------------------------------------
def get_neccessary_params(func):
    """"""
    assert callable(func), '[!] The [func] you input cannot be called!'
    
    result = []
    
    table = get_args_dict(func)['args']['args_table']
    for i in list(table.items()):
        if i[1] != None:
            pass
        else:
            result.append(i[0])
            
    return result
    



#----------------------------------------------------------------------
def get_classes(mod, metaclass=None):
    """"""
    if metaclass == None:
        metaclass = tuple([types.TypeType, types.ClassType])
    for i in get_callables(mod):
        if isinstance(i, metaclass):
            yield i
        
if __name__ == '__main__':
    unittest.main()