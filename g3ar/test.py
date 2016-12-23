#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar Test
  Created: 2016/12/23
"""

import unittest

from time import sleep
from threadutils import thread_pool, contractor
from Queue import Empty
ThreadPool = thread_pool.Pool
Contractor = contractor.Contractor

########################################################################
class G3arSubModuleTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_threadpool(self):
        """"""
        
        def testthreadpool_function(arg1, arg2='adsf'):
            sleep(1)
            return arg1, arg2

        pool = ThreadPool(thread_max=30)

        pool.start()

        for i in range(40):
            pool.feed(testthreadpool_function, arg1=i)


        result_gen = pool.get_result_generator()
        for i in result_gen:
            print pool.task_count
            print pool.executed_task_count
            print pool.percent            
            print i


        for i in range(21,41):
            pool.feed(testthreadpool_function, arg1=i)


        result_queue = pool.get_result_queue()

        while True:
            try:
                print result_queue.get(timeout=2)
            except Empty:
                print 'End!'
                break
    
    #----------------------------------------------------------------------
    def test_contractor(self):
        """"""
        
        def testcontractor_function(arg1, arg2='adsf'):
            sleep(1)
            return arg1, arg2

        ctr = Contractor(thread_max=30)
    
        for i in range(40):
            ctr.feed(testcontractor_function, arg1=i)
        
        ctr.start()
    
        result_gen = ctr.get_result_generator()

            # Generator 的使用方法
        for i in result_gen:
            print i

        ctr = Contractor(thread_max=50)

        def testcontractor_function_ecp(arg1, arg2='adsf'):
            sleep(1)
            raise Exception('test exception')
            #return arg1, arg2
        
        for i in range(41, 81):
            ctr.feed(testcontractor_function_ecp, arg1=i)
    
        ctr.start()

            
        result_queue = ctr.get_result_queue()
    
        while True:
            try:
                print result_queue.get(timeout=2)
            except Empty:
                print 'End!'
                break
        
        


if __name__ == '__main__':
    unittest.main()
