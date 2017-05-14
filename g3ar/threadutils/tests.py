#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Tester For Threadpoolex
  Created: 05/13/17
"""

import unittest
import queue
import time
from threadpoolex import ThreadPoolXLabor, ThreadPoolX, _LaborFactory

#----------------------------------------------------------------------
def test_task_error(arg1, arg2=4):
    """"""
    time.sleep(3)
    1/0
    return arg1, arg2

#----------------------------------------------------------------------
def test_task(arg1, arg2=4):
    """"""
    time.sleep(3)
    return arg1, arg2


########################################################################
class ThreadPoolExTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_labor(self):
        """"""
        def _labor_callback(result):
            raise ValueError()
            #_retqueue.put(result)

        def _labor_callback_exc(result):
            _retqueue.put(result)

        def _task_exc_handle(e):
            _retqueue.put((1,4))
            print e

        _retqueue = queue.Queue(1)
        s = ThreadPoolXLabor('test')
        s.add_task_exception_callback(_task_exc_handle)
        s.add_callback(_labor_callback, _labor_callback_exc)

        s.start()
        s.execute(test_task, var_args=(1,), keyword_args={})

        _resultTuple = _retqueue.get()
        self.assertTrue(_resultTuple[0] == 1)
        self.assertEqual(_resultTuple[1], 4)

        s.quit()
        time.sleep(1)


    #----------------------------------------------------------------------
    def test_pool(self):
        """"""
        quited = False
        def print_result(result):
            if result[0] == 5:
                print('prepared exiting')
                time.sleep(1)
                print('quit!')
                quited = True
            print result
        pool = ThreadPoolX()
        pool.add_callbacks(callback=print_result)
        for i in range(16):
            pool.feed(target=test_task, vargs=(i,))
        pool.start()

        def target():
            time.sleep(1)
            return 'h'

        def anothor_result(result):
            if result == 'h':
                print 'target with callback success!'

        pool.feed_with_callback(target, callback=anothor_result)
        time.sleep(6)
        pool.quit()

    #----------------------------------------------------------------------
    def test_laborfactory(self):
        """"""
        lf = _LaborFactory(debug=True, loop_interval=0.2)

        def _labor_callback(result):
            raise ValueError()
            #_retqueue.put(result)

        def _labor_callback_exc(result):
            _retqueue.put(result)

        def _task_exc_handle(e):
            _retqueue.put((1,4))
            print e

        _retqueue = queue.Queue(1)        
        lf.add_callbacks(_labor_callback, _labor_callback_exc)
        lf.add_exception_callback(_task_exc_handle)
        new_labor = lf.build_labor()

        self.assertIsInstance(new_labor, ThreadPoolXLabor)

        new_labor.start()
        new_labor.execute(test_task)
        new_labor.execute(test_task_error)
        new_labor.quit()


if __name__ == '__main__':
    unittest.main()