#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Python Ping
  Created: 2016/12/26
"""

import unittest
from .isalive import is_alive

#----------------------------------------------------------------------
def pyping(target, timeout=2, count=4):
    """"""
    return is_alive(target)
    

if __name__ == '__main__':
    unittest.main()