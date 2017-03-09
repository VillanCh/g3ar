#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: iter mix
  Created: 03/09/17
"""

import unittest
import ast

forcode_tmp = """
for {valuebase}{index} in {iterbase}{index}:
    pass
try:
    {iterbase}{index}.reset() # {last_index}
except AttributeError:
    pass
"""

yieldcode_tmp = """
yield tuple([{content}])
"""

define_tmp = """
{iterbase}{index} = args[{index}]
"""

func_tmp = """
def dynamic_func(*args):
    pass
"""

mod_tmp = """
"""

mod = ast.parse(mod_tmp, '<string>', 'exec')


ITERBASE = 'arg_'
VALUEBASE = 'i_'

#
# compact components to a function
#----------------------------------------------------------------------
def _compact_dynamic_func(body):
    """"""
    mod = ast.parse(func_tmp, '<string>')
    funcnode = mod.body[0]
    funcnode.body.pop()
    for i in body:
        funcnode.body.append(i)
    
    return funcnode

#
# render the for code
#----------------------------------------------------------------------
def _render_for(iter_id_base, value_id_base, index, filled_expr=None):
    """"""
    iter_id_base = str(iter_id_base)
    value_id_base = str(value_id_base)
    index = int(index)
    lastindex = index if index - 1 < 0 else index - 1  
    
    _tmp = forcode_tmp.format(valuebase=value_id_base,
                              index=index,
                              iterbase=iter_id_base,
                              last_index=lastindex)
    
    _body = ast.parse(_tmp, '<string>').body
    _for = _body[0]
    
    if filled_expr:
        _for.body.pop()
        if isinstance(filled_expr, (list, tuple)):
            for i in filled_expr:
                _for.body.append(i)
        else:
            _for.body.append(filled_expr)
    return _body
    

#----------------------------------------------------------------------
def _render_yield(base, length):
    """"""
    base = str(base)
    length = int(length)
    ret = []
    for i in range(length):
        ret.append((base + '{}').format(i))
    yieldcode_new = yieldcode_tmp.format(content=','.join(ret))
    #print yieldcode_new
    return ast.parse(yieldcode_new, '<string>').body.pop()

#
# section2 yield
#----------------------------------------------------------------------
def _render_core_block(iter_num, iter_namebase=ITERBASE, value_namebase=VALUEBASE):
    """"""
    last = None
    for i in range(iter_num):
        i = iter_num - i - 1
        if last == None:
            last = _render_for(iter_namebase, value_namebase, i, _render_yield(value_namebase, iter_num))
        else:
            last = _render_for(iter_namebase, value_namebase, i, last)
    
    last = last[0]
    return last

#
# section1 define
#----------------------------------------------------------------------
def _define_iter(iterbase, length):
    """"""
    defnieblock = []
    for i in range(length):
        define_new = define_tmp.format(index=i, iterbase=iterbase)
        definebody = ast.parse(define_new, '<string>').body.pop()
        defnieblock.append(definebody)
    
    return defnieblock


#----------------------------------------------------------------------
def iter_mix(*args):
    """"""
    length = len(args)
    basebody = _define_iter(ITERBASE, length)
    basebody.append(_render_core_block(iter_num=length))
    funcmod = _compact_dynamic_func(basebody)
    mod_tmp = """
    """
    
    mod = ast.parse(mod_tmp, '<string>', 'exec')
    
    astt = funcmod
    if not isinstance(astt, (list, tuple)):
        mod.body.append(astt)
    else:
        for i in astt:
            mod.body.append(i)    
    
    exec(compile(mod, '<string>', 'exec'))
    return dynamic_func(*args)


if __name__ == '__main__':
    unittest.main()