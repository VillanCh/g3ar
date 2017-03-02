#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 03/02/17
"""

import unittest
import re


#
# Domain reg pattern
#
DOMAIN_REG = '(?i)(([a-z0-9-]+)((\.[0-9a-z-]+)+))'

#
# URL reg pattern
#
URL_REG = '(^(([a-z]+)://)(' + DOMAIN_REG + ')((\/([a-zA-Z0-9-\.]+)?)+)?)'

#
# IP REG
#
IPv4_REG = "((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9]))"
IPv6_REG = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

#----------------------------------------------------------------------
def is_url(target):
    """"""
    if len(re.findall(pattern=URL_REG, string=target)) > 0:
        return True
    else:
        return False
    
#----------------------------------------------------------------------
def is_ipv4(target):
    """"""
    if len(re.findall(pattern=IPv4_REG, string=target)) > 0:
        return True
    else:
        return False

#----------------------------------------------------------------------
def is_ipv6(target):
    """"""
    if len(re.findall(pattern=IPv6_REG, string=target)) > 0:
        return True
    else:
        return False
    
    
#----------------------------------------------------------------------
def is_domain(target):
    """"""
    if len(re.findall(pattern=DOMAIN_REG, string=target)) > 0:
        return True
    else:
        return False
    

########################################################################
class ValidatorTester(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_check_url(self):
        """"""
        url1 = 'ftp://blog.tbis.me/adfa/a/df/a'
        url2 = 'hTtP://bot-as.adf.ad.a/'
        
        self.assertTrue(is_url(url1))
        self.assertTrue(is_url(url2))
    
    #----------------------------------------------------------------------
    def test_check_ip(self):
        """"""
        
        IPv4 = '12.3.2.3'
        IPv6 = '2001:0db8:85a3:08d3:1319:8a2e:0370:7344'
        
        self.assertTrue(is_ipv4(IPv4))
        self.assertTrue(is_ipv6(IPv6))
        
    #----------------------------------------------------------------------
    def test_check_domain(self):
        """"""
        domain1 = 'demo.com'
        domain2 = 'vill1nch.top'
        
        
        self.assertTrue(is_domain(domain1))
        self.assertTrue(is_domain(domain2))
    


if __name__ == '__main__':
    unittest.main()