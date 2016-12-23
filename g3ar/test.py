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
from taskbulter import task_bulter
from Queue import Empty
ThreadPool = thread_pool.Pool
Contractor = contractor.Contractor
TaskBulter = task_bulter.TaskBulter

def tasktest(arg1):
    print(arg1)
    def runforever():
        while True:
            pass
    
    pool = ThreadPool()
    pool.start()
    pool.feed(runforever)
    pool.feed(runforever)
    pool.feed(runforever)
    while True:
        pass

########################################################################
class G3arThreadUtilsTest(unittest.case.TestCase):
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
        
        


########################################################################
class G3arTaskBulterTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_taskbulter(self):
        """Constructor"""
        bulter = TaskBulter(threads_update_interval=0.1)
            
        bulter.start_task(id='tasktest', target=tasktest, args=(5,))
        task = bulter.get_task_by_id('tasktest')
        print task
        sleep(2)
        print bulter.get_tasks_status()
        bulter.destory_task(task)
        #bulter.close()
    
    
if __name__ == '__main__':
    unittest.main()
