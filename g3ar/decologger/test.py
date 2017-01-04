#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for decologger
  Created: 2016/12/18
"""

import unittest
import traceback
from .decologger import Decologger


########################################################################
class DecologgerTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_learn_decorector(self):
        """"""
        print(('='*64))
        def logit(func):
            def wrapper(*args, **kwargs):
                print(('wrapper got param', args, kwargs))
                print(('pre call', func.__name__))
                return func(*args, **kwargs)
            return wrapper
    
        #----------------------------------------------------------------------
        @logit
        def funct(args):
            """"""
            print(('funct called! Got Param', args))
        
        funct('Hello')
        
        def sss(*arg):
            print(arg)
            print('sssss called') 
            return logit(arg[0])
        
        @sss
        def tests():
            print('tests called')
        
        tests()
        
        print(('='*64))
    
    def test_exception(self):
        try:
            raise Exception('adfasdfasdf')
        except:
            print(traceback.extract_stack())
            traceback.format_exc()
    
    #----------------------------------------------------------------------
    def test_decologger_basic_api(self):
        """"""
        dclogger = Decologger(name='testlogger')
        
        
        class A(object):
            #----------------------------------------------------------------------
            def __init__(self):
                """"""
                pass
            
            #----------------------------------------------------------------------
            @dclogger.crucial
            def B(self):
                """"""
                print('B Called!')
        
        
        dclogger.critical('Hello Critical')
        A().B()
                
        
        print(('='*64))
        
        
        
    
    

if __name__ == '__main__':
    unittest.main()