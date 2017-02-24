#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: example for taskbulter
  Created: 02/24/17
"""

import unittest

#
# example for taskbulter
#
import time
from g3ar import TaskBulter
from g3ar.utils.print_utils import print_bar

tbr = TaskBulter()

taskid = 'testtask-id'
#----------------------------------------------------------------------
def func(arg1, arg2='1'):
    """"""
    time.sleep(2)
    return arg1, arg2
    

print_bar('start the task')
print(tbr.start_task(id=taskid, target=func, args=('arg1var',)))

print_bar('watch the status')
print(tbr.get_tasks_status())

time.sleep(3)

print_bar('get result')
print(tbr.get_result(taskid))

if __name__ == '__main__':
    unittest.main()