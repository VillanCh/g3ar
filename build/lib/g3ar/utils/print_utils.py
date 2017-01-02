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
        bar_side = basic_char * length_one_side
        bar = bar_side + text + bar_side
    else:
        bar = basic_char * length

    if color and hasattr(Fore, color.upper()):
        bar = getattr(Fore, color.upper()) + bar
    else:
        bar = bar
        
    print(bar)
    


if __name__ == '__main__':
    unittest.main()