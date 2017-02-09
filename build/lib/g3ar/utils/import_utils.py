#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Import Utils
  Created: 2017/1/2
"""

import unittest
import os
import sys

#----------------------------------------------------------------------
def import_by_path(path, module_name, basedir='.'):
    """"""
    dirname = os.path.dirname(basedir)
    absdir = os.path.abspath(dirname)
    absdir = os.path.join(absdir, path)
    sys.path.append(absdir)
    mod = __import__(module_name)
    sys.path.remove(absdir)
    
    return mod

if __name__ == '__main__':
    unittest.main()