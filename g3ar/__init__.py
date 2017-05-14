#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar entry
  Created: 2016/12/20
"""

import unittest

from .threadutils.thread_pool import Pool as ThreadPool
from .threadutils.threadpoolex import ThreadPoolX
from .threadutils.contractor import Contractor
from .decologger.decologger import Decologger as DecoLogger
from .dict_parser.dict_parser import DictParser
from .dict_parser.dict_parser_from_iter import DictParserFromIter
from .taskbulter.task_bulter import TaskBulter
from .dict_parser.dict_parser_mixer import DictParserMixer
#from .utils import ip_calc_utils
from .utils.pyping import pyping
from .utils.iter_utils import iter_mix

#----------------------------------------------------------------------
def ping(host, timeout=2, count=4):
    """"""
    return pyping(host, timeout, count)

#----------------------------------------------------------------------
def dict_parser_mixer_func(*args):
    """"""
    for i in args:
        assert isinstance(i, DictParser)
    
    return iter_mix(*args)
    