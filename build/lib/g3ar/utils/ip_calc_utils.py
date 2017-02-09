#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Caculate About IP using IPy
  Created: 2016/12/26
"""

import unittest

from IPy import IP
#from .ipwhois import IPWhois
from random import randint, seed
from time import time

seed(time())


#----------------------------------------------------------------------
def is_ipv4(ip):
    """Check if the [ip] is a real ip addr.
    
    Params:
        ip: :str: General IP format.
        
    Returns:
        :type: bool
        :desc: if ip is a valid IP addr, return true
            else return False"""
    try:
        IP(ip)
        return True
    except ValueError:
        return False

#----------------------------------------------------------------------
def get_all_c_class(ip):
    """Return the All C Class Addr (v4)"""
    for i in IP(ip).make_net('255.255.255.0'):
        yield i.strNormal()
    
#----------------------------------------------------------------------
def ip2int(ip):
    """"""
    return IP(ip).int()

#----------------------------------------------------------------------
def ipv4_range(start_ip, end_ip):
    """"""
    start = ip2int(start_ip)
    end = ip2int(end_ip)
    
    for i in range(start, end):
        yield IP(i).strNormal()
    
#----------------------------------------------------------------------
def random_ip(start='0.0.0.0', end='224.0.0.0'):
    """"""
    return IP(randint(IP(start).int(), IP(end).int())).strNormal()
    

if __name__ == '__main__':
    unittest.main()