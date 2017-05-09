#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Gen A DictParser from a iter
  Created: 05/08/17
"""

from dict_parser import DictParser

########################################################################
class DictParserFromObject(DictParser):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, obj, *vs, **kw):
        """Constructor"""
        self.obj = obj
        
        self._index = 0
        
    #----------------------------------------------------------------------
    def __enter__(self):
        """"""
        return
    
    #----------------------------------------------------------------------
    def __exit__(self):
        """"""
        return 
    
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        return self

    #----------------------------------------------------------------------
    def __next__(self):
        """"""
        return self._next()
    
    #----------------------------------------------------------------------
    def next(self):
        """"""
        return self._next()
        
        
        
        
        
        
        
    
    