#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: threads utils
  Created: 03/07/17
"""

import unittest
import threading

#----------------------------------------------------------------------
def start_new_thread(target, name=None, args=tuple(), 
                     kwargs={}, daemon=True):
    """"""
    ret = threading.Thread(target=target, args=args, 
                           kwargs=kwargs, name=name)
    ret.daemon = daemon
    ret.start()
    return ret
    
    

if __name__ == '__main__':
    unittest.main()