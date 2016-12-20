#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Provide some useful thread utils
  Created: 2016/10/29
"""

import unittest
#import multiprocessing 
from pprint import pprint
from time import sleep
from Queue import Full, Empty, Queue
#from random import choice
#from traceback import format_exc
from threading import Thread
#from multiprocessing import Process, Lock

########################################################################
class TaskError(Exception):
    """"""
    pass
        
########################################################################
class LaborThread(Thread):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, result_queue, *args, **kargs):
        """Constructor"""
        Thread.__init__(self, *args, **kargs)
        
        self._result_queue = result_queue
    
        self._startworkingflag_ = True
        
        self._task_queue = Queue(1)
    
    #----------------------------------------------------------------------
    def get_result_queue(self):
        """"""
        return self._result_queue
        
    #----------------------------------------------------------------------
    def get_task_queue(self):
        """"""
        return self._task_queue
    
    #----------------------------------------------------------------------
    def feed(self, function, *vargs, **kwargs):
        """"""
        try:
            self._task_queue.put_nowait(tuple([function, vargs, kwargs]))
            return True
        except Full:
            #format_exc()
            return False
    
    #----------------------------------------------------------------------
    def run(self):
        """"""
        while self._startworkingflag_:
            #pprint('Running')
            try:
                _task = self._task_queue.get(timeout=3)
                result = {}
                result['from'] = self.name
                result['state'] = False
                result['result'] = None
                result['current_task'] = _task.__str__()
                result['exception'] = tuple()
                try:
                    ret = self._process_task(_task)
                    result['state'] = True
                    result['result'] = ret
                    self._result_queue.put(result)                    
                except Exception, e:
                    result['state'] = False
                    result['result'] = None
                    exception_i = (str(type(e)), str(e))
                    result['exception'] = exception_i
                    self._result_queue.put(result)

            except Empty:
                pass
    
    #----------------------------------------------------------------------
    def _process_task(self, task):
        """"""
        try:
            ret = task[0](*task[1], **task[2])
            return ret 
        except Exception, e:
            raise e
            
        
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        #self.stop()
        self._startworkingflag_ = False
    
    #----------------------------------------------------------------------
    def __del__(self):
        """"""
        self.stop()
        
    #----------------------------------------------------------------------
    def _exception_process(self):
        """"""
        
    

########################################################################
class Pool(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, thread_max=30):
        """Constructor"""
        self.thread_max = thread_max
        
        self._current_thread = []
        self._daemon_thread = []
        
        self._result_queue = Queue()
        
        self._task_queue = Queue()
        
        self.is_alive = True
        
    #----------------------------------------------------------------------
    def _restart_thread_daemon(self):
        """"""
        #pprint('threads daemon started!')
        while self.is_alive:
            if len(self._current_thread) < self.thread_max:
                self._start_new_labor()
            else:
                sleep(0.5)
    
    #----------------------------------------------------------------------
    def _start_new_labor(self):
        """"""
        #pprint('start new labor')
        _tmp_labor = LaborThread(result_queue=self._result_queue)
        _tmp_labor.start()
        self._current_thread.append(_tmp_labor)
        
    #----------------------------------------------------------------------
    def feed(self, target_func, *vargs, **kwargs):
        """"""
        self._task_queue.put(tuple([target_func, vargs, kwargs]))
        
    #----------------------------------------------------------------------
    def _dispatcher(self):
        """"""
        #pprint('dispatcher start!')
        while self.is_alive:
            try:
                ret = self._task_queue.get()
                while True:
                    availible_threads = map(lambda x: None if x.get_task_queue().full() else x, 
                                            self._current_thread)
                    for i in availible_threads:
                        if i == None:
                            pass
                        else:
                            i.feed(ret[0], *ret[1], **ret[2])
                            ret = None
                            break
                    if ret == None:
                        break
                    else:
                        continue
            except Empty:
                sleep(seconds=0.5)
        
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        for i in self._current_thread:
            i.stop()
            del i
        self.is_alive = False
        
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self.is_alive = True
        
        _ = Thread(name='restart_labor_daemon', target=self._restart_thread_daemon)
        _.daemon = True
        _.start()
        self._daemon_thread.append(_)
        
        _ = Thread(name='dispatcher_daemon', target=self._dispatcher)
        _.daemon = True
        _.start()

        
    #----------------------------------------------------------------------
    def get_result_queue(self):
        """"""
        return self._result_queue
    
    #----------------------------------------------------------------------
    def get_task_queue(self):
        """"""
        return self._task_queue
        
        
                    


########################################################################
class PoolTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        self.test_laborprocess()

    #----------------------------------------------------------------------
    def test_laborprocess(self):
        """"""
        def func(arg1):
            print 'function called'
            return arg1
        
        rq = Queue()
        lp = LaborThread(result_queue=rq)
        lp.daemon = True
        lp.start()
        lp.feed(func, 1234)
        sleep(3)
        _ = lp.get_result_queue().get()
        self.assertTrue(_['state'])
        self.assertEqual(_['result'], 1234)
        
    #----------------------------------------------------------------------
    def test_pool(self):
        """"""
        def func1(arg1):
            print 'func1 called!'
            return arg1
            
        pool = Pool()
        pool.start()
        pool.feed(func1, 12345)
        for i in xrange(10):
            pool.feed(func1, i)
        sleep(3)
        while True:
            try:
                pprint(pool.get_result_queue().get(timeout=5))
            except Empty:
                break
            
        pool.stop()
if __name__ == "__main__":
    unittest.main()