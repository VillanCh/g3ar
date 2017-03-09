#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar entry
  Created: 2016/12/20
"""

import unittest

from .threadutils import thread_pool
from .threadutils import contractor
from .decologger import decologger
from .dict_parser import dict_parser
from .taskbulter import task_bulter
#from .utils import ip_calc_utils
from .utils.pyping import pyping
from .utils.iter_utils import iter_mix

ThreadPool = thread_pool.Pool
Contractor = contractor.Contractor
DictParser = dict_parser.DictParser
DecoLogger = decologger.Decologger
TaskBulter = task_bulter.TaskBulter
#IPv4CalcUtils = ip_calc_utils


#----------------------------------------------------------------------
def ping(host, timeout=2, count=4):
    """"""
    return pyping(host, timeout, count)

#----------------------------------------------------------------------
def dict_parser_mixer(*args):
    """"""
    for i in args:
        assert isinstance(i, DictParser)
    
    return iter_mix(*args)
    