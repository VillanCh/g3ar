#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 02/24/17
"""

import unittest

from g3ar import DictParser
from g3ar.utils.print_utils import print_bar

dparser = DictParser(filename='demodict', session_id='demosession')

#
# First 10 LINE
#
print_bar('GET 10 LINES')
for i in xrange(10):
    print(dparser.next())
print_bar('END')
print()

dparser.force_save()

del dparser

dparser_continue = DictParser(filename='demodict', session_id='demosession', do_continue=True)
#
# Next Lines
#
print_bar('GET NEXT ALL LINE')
for i in dparser_continue:
    print(i)

if __name__ == '__main__':
    unittest.main()