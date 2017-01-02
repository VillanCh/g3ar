#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for utils
  Created: 2017/1/2
"""

import unittest
import ip_calc_utils
from ip_calc_utils import *
from print_utils import print_bar
from inspect_utils import *
from import_utils import import_by_path


########################################################################
class PrintBarTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        print_bar('WellCome TO MY G3ar')
        print_bar(basic_char='0')
        print_bar(color='red')
    
########################################################################
class InspectUtilsTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        ret = get_args_dict(ip_calc_utils.ip2int)
        pprint(ret)
        ret = get_neccessary_params(ip_calc_utils.ipv4_range)
        pprint(ret)        
        ret = get_callables(ip_calc_utils)
        pprint(ret)
        ret = get_fileds(ip_calc_utils)
        pprint(ret)
        ret = get_methods(ip_calc_utils)
        pprint(ret)
        ret = get_functions(ip_calc_utils)
        pprint(ret)  
        
########################################################################
class IPutilcTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_little_utils(self):
        """"""
        print is_ipv4('45.78.65.21')
        for i in get_all_c_class('222.45.35.4'):
            #print i
            pass
        
        get_ip_block_from_ipwhois('222.45.35.4')
                  
        for i in ipv4_range('124.5.2.3','124.5.3.9'):
            print i
        
        for i in range(20):
            print random_ip()
        
########################################################################
class ImportUtilsTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_import_utils(self):
        """Constructor"""
        
        print(import_by_path('..', 'dict_parser'))        
    
    
    
if __name__ == '__main__':
    unittest.main()