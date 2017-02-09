#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v11l4n>
  Purpose: Print Better Helper!
  Created: 2017/1/2
"""

import unittest
from colorama import init, Fore

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

if __name__ == '__main__':
    unittest.main()