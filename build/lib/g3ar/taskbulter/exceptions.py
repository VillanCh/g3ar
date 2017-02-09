#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Many Exceptions
  Created: 2016/12/12
"""

import unittest


########################################################################
class TaskRuntimeError(Exception):
    """"""
    pass



########################################################################
class TaskCannotBeCalled(Exception):
    """"""
    pass


########################################################################
class ExistedTaskId(Exception):
    """"""
    pass




if __name__ == '__main__':
    unittest.main()