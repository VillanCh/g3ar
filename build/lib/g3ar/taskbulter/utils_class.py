#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Utils Classes
  Created: 2016/12/13
"""

import unittest


########################################################################
class Singleton(object):
    """"""
    #_instance = None

    #----------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """singleton class wrapper"""
        if not hasattr(cls, '_instance'):
            origin = super(Singleton, cls)
            cls._instance = origin.__new__(cls, *args, **kwargs)
        return cls._instance
        
    
    
if __name__ == '__main__':
    unittest.main()