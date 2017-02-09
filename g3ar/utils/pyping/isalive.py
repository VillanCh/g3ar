#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test the host is alive?
  Created: 2016/12/20
"""

import unittest
from .ping import verbose_ping

#----------------------------------------------------------------------
def is_alive(host, timeout=2, count=4):
    """"""
    result = {}
    
    ret = ping_host(host, timeout, count)
    result['ping'] = ret
    
    return result


#----------------------------------------------------------------------
def ping_host(host, timeout=2, count=4):
    """"""
    result = {}
    result['alive'] = False
    result['delay'] = 0
    try:
        ping_delay = verbose_ping(host, timeout=timeout,count=count)
        if ping_delay != 0:
            result['alive'] = True
            result['delay'] = ping_delay
            return result
        else:
            raise ValueError()
    except:
        return result


########################################################################
class IsAliveTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_pingtest(self):
        """Ping test"""
        
        print(ping_host('45.78.6.64'))
        
        
    
    

if __name__ == '__main__':
    unittest.main()