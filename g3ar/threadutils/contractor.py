#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Provide some useful thread utils
  Created: 2016/10/29
"""
import uuid
import time
import unittest
try:
    from queue import Queue, Empty
except:
    from Queue import Queue, Empty
import threading
from threading import Thread
import inspect
import traceback


#----------------------------------------------------------------------
def start_thread(func, *args, **kwargs):
    """"""
    ret = Thread(target=func, args=args, kwargs=kwargs)
    ret.daemon = True
    ret.start()


########################################################################
class Contractor(object):
    """Create Multi-Thread to support the 
    concurrence of many tasks"""

    #----------------------------------------------------------------------
    def __init__(self, thread_max=50):
        """Constructor"""
        self.task_list = []
        self.result_queue = Queue()

        self.lock = threading.Lock()

        self.thread_max = thread_max
        self._current_thread_count = 0
        
        self._executed_task_count = 0
        self._task_count = 0

    def _uuid1_str(self):
        '''Returns: random UUID tag '''
        return str(uuid.uuid1())

    #----------------------------------------------------------------------
    def feed(self, target_func, *vargs, **kwargs):
        """"""
        self.add_task(target_func, *vargs, **kwargs)
        
    def add_task(self, target_func, *args, **argv):
        '''Add task to Pool and wait to exec

        Params:
            target_func : A callable obj, the entity of the current task
            args : the args of [target_func]
            argv : the argv of [target_func]
        '''
        assert callable(target_func), '[!] Function can \'t be called'

        ret = {}
        ret['func'] = target_func
        ret['args'] = args
        ret['argv'] = argv
        #ret['uuid'] = self.signal_name
        self._task_count = self._task_count + 1
        self.task_list.append(ret)

    def start(self):
        """"""
        ret = Thread(target=self._run)
        ret.daemon = True
        ret.start()

        return self.result_queue

    #----------------------------------------------------------------------
    def _run(self):
        """"""
        for i in self.task_list:
            #print self.current_thread_count
            while self.thread_max <= self._current_thread_count:
                time.sleep(0.3)
            self._start_task(i)        

    def _start_task(self, task):
        """"""
        self._current_thread_count = self._current_thread_count + 1
        try:

            ret = Thread(target=self._worker, args=(task,))
            ret.daemon = True
            ret.start()
        except TypeError:
            self._current_thread_count = self._current_thread_count - 1

    def _worker(self, dictobj):
        """"""
        func = dictobj['func']
        args = dictobj['args']
        argv = dictobj['argv']

        try:
            result = func(*args, **argv)
        except Exception as e:
            #print 'ecp occured'
            result = tuple([e, traceback.extract_stack()])
        
        self.lock.acquire()
        self._executed_task_count = self._executed_task_count + 1
        self._add_result_to_queue(result=result)
        self.lock.release()

    def _add_result_to_queue(self, **kw):
        """"""
        assert 'result' in kw, '[!] Result Error!'

        self.result_queue.put(kw['result']) 
        self._current_thread_count = self._current_thread_count - 1
        
    #----------------------------------------------------------------------
    def get_result_queue(self):
        """"""
        return self.result_queue

    #----------------------------------------------------------------------
    def get_task_list(self):
        """"""
        self.task_list
    
    #----------------------------------------------------------------------
    def get_result_generator(self):
        """"""
        while True:
            try:
                ret = self.result_queue.get(timeout=1)
                yield ret
            except Empty:
                if self._task_count == self._executed_task_count:
                    break
                else:
                    pass        
    
    #----------------------------------------------------------------------
    @property
    def task_count(self):
        """"""
        return self._task_count
    
    #----------------------------------------------------------------------
    @property
    def executed_task_count(self):
        """"""
        return self._executed_task_count
    
    #----------------------------------------------------------------------
    @property    
    def percent(self):
        """"""
        return float(self._task_count)/float(self._executed_task_count)
    
    #----------------------------------------------------------------------
    @property
    def current_thread_count(self):
        """"""
        return self._current_thread_count
        
        
        


class UtilsTest(unittest.case.TestCase):
    def runTest(self):
        ms = inspect.getmembers(self)
        ms = [x[0] for x in ms]
        for i in ms:
            if callable(getattr(self,i)):
                if i.startswith('test_'):
                    getattr(self, i)()    

    def test_pool(self):
        def demo_task(*args):
            '''simulate the plugin.run'''
            print('[!] Computing!')
            time.sleep(args[0])
            print('[!] Finished!')
            print()
            returns = 'Runtime Length : %s' % str(args)
            return returns
        pool = Contractor()
        pool.add_task(demo_task, 7)
        pool.add_task(demo_task, 3)
        q = pool.start()
        print(pool._current_thread_count)
        self.assertIsInstance(q, Queue)

        r = q.get()
        print(r)
        self.assertIsInstance(r, str)
        r = q.get()
        print(r)
        self.assertIsInstance(r, str)

        print(pool._current_thread_count)


if __name__ == '__main__':
    unittest.main()