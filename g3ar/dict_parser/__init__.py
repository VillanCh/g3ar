#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Simple and Quick Parse your dictionary FOR TENTEST PROGRAMMER!
  Created: 2016/12/16
"""

from . import dict_parser
from .dict_parser import *
from .dict_parser_mixer import DictParser
from .dict_parser_from_iter import DictParserFromIter

def get_dictparser(filename, 
                   session_id=DEFAULT_SESSION_ID, 
                   do_continue=False,
                   session_data_file=SESSION_TABLE_FILE):
    return DictParser(filename, session_id, do_continue, session_data_file)


    