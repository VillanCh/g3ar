#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: TestForDictParser
  Created: 2016/12/16
"""

import unittest
from .dict_parser import *


########################################################################
class DictParserTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_dict_basic_api(self):
        """Constructor"""
        pprint('='*64)
        pprint('Test Dict Parser Parse A Small Dictionary')
        dictparse = DictParser(filename='dir.txt', do_continue=False)
        
        count = 0
        for i in dictparse:
            pprint(i)
            count = count + 1
            if count > 10:
                break
            
        dictparse = DictParser(filename='dir.txt', do_continue=True)
        retcollect = dictparse.get_next_collection(num=200)
        
        for i in retcollect:
            pprint(i)
        pprint('='*64)
    
    #----------------------------------------------------------------------
    def test_get_an_collection(self):
        """"""
        
        pprint('='*64)
        pprint('Test get a collection by dictparser')
        dictparse = DictParser(filename='dir.txt', do_continue=False)
        retcollect = dictparse.get_next_collection(num=200)
        
        for i in retcollect:
            pprint(i)
        pprint('='*64)
        
    #----------------------------------------------------------------------
    def test_get_basic_information(self):
        """"""
        pprint('='*64)
        pprint('Test get basic information of dictfile')
        dictparse = DictParser(filename='dir.txt', do_continue=False)
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())
        dictparse.get_fp().readline()
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())  
        #dictparse.reset()
        dictparse.get_fp().readline()
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())        
        pprint('='*64)
        

if __name__ == '__main__':
    unittest.main()