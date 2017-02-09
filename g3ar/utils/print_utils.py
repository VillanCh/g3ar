#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v11l4n>
  Purpose: Print Better Helper!
  Created: 2017/1/2
"""

import unittest
from colorama import init, Fore
from prettytable import PrettyTable

#----------------------------------------------------------------------
def print_bar(text=None, basic_char='=', length=70, color=None):
    """"""
    if text:
        text = str(text)
        textlen = len(text)
        length_one_side = (length - textlen) / 2
        bar_side = basic_char * int(length_one_side)
        bar = bar_side + text + bar_side
    else:
        bar = basic_char * length

    if color and hasattr(Fore, color.upper()):
        bar = getattr(Fore, color.upper()) + bar
    else:        
        bar = bar
    
    init(autoreset=True)
    print(bar)

#----------------------------------------------------------------------
def print_red(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.RED + raw))

#----------------------------------------------------------------------
def print_green(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.GREEN + raw))

#----------------------------------------------------------------------
def print_blue(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.CYAN + raw))
    
#----------------------------------------------------------------------
def print_yellow(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.YELLOW + raw))  

#----------------------------------------------------------------------
def print_cyan(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.CYAN + raw))  

#----------------------------------------------------------------------
def print_purpul(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.MAGENTA + raw))

#----------------------------------------------------------------------
def print_gray(*args):
    """"""
    raw = str(args)
    init(autoreset=True)
    print((Fore.LIGHTBLACK_EX + raw))
    

#----------------------------------------------------------------------
def print_column(head, column, color=''):
    """Print Column With Color.
    
    Params:
        head: :: A head for the column data.
        column: :list tuple: the column data(list or tuple)
        coler: :str: 
            lightblack_ex
            magenta
            cyan
            green
            blue
            yellow
            red
    
    Returns:
        return the strings of table 
    """
    assert isinstance(color, str)
    
    _prefix = ''
    if hasattr(Fore, color.upper()):
        _prefix = getattr(Fore, color.upper())
    
    table = PrettyTable()
    table.add_column(head, column)
    
    raw = table.get_string()
    init(autoreset=True)
    print(_prefix + raw)
    return table

#----------------------------------------------------------------------
def print_columns(heads, columns, color=''):
    """Print Column With Color.
    
    Params:
        head: :: A list of heads for the columns data.
        column: :list tuple: the column data(list or tuple)
        coler: :str: 
            lightblack_ex
            magenta
            cyan
            green
            blue
            yellow
            red
    
    Returns:
        return the strings of table 
    """
    assert isinstance(color, str)
    assert len(heads) == len(columns)
    
    _prefix = ''
    if hasattr(Fore, color.upper()):
        _prefix = getattr(Fore, color.upper())
    
    table = PrettyTable()
    for i in xrange(len(heads)):
        head = heads[i]
        column = columns[i]
        table.add_column(head, column)
    
    raw = table.get_string()
    init(autoreset=True)
    print(_prefix + raw)
    return table    
    
#----------------------------------------------------------------------
def print_rows(heads, rows, color=''):
    """Print Column With Color.
    
    Params:
        heads: :list: the row of heads
        rows: :list tuple: the rows data(list or tuple)
        coler: :str: 
            lightblack_ex
            magenta
            cyan
            green
            blue
            yellow
            red
    
    Returns:
        return the strings of table 
    """
    assert len(heads) == len(rows[0])
    assert isinstance(color, str)
    
    _prefix = ''
    if hasattr(Fore, color.upper()):
        _prefix = getattr(Fore, color.upper())
    
    #
    # split rows
    #
    table = PrettyTable(heads)
    for row in rows:
        table.add_row(row)
    
    
    raw = table.get_string()
    init(autoreset=True)
    print(_prefix + raw)
    return table        



if __name__ == '__main__':
    unittest.main()