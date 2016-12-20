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
from Queue import Queue
import threading
from threading import Thread
import inspect


#----------------------------------------------------------------------
def start_thread(func, *args, **kwargs):
    """"""
    Thread(target=func, args=args, kwargs=kwargs).start()


########################################################################
class Contractor(object):
    """Create Multi-Thread to support the 
    concurrence of many tasks"""

    #----------------------------------------------------------------------
    def __init__(self, thread_max=50):
        """Constructor"""
        self.task_list = []
        self.result_queue = Queue()

        self.signal_name = self._uuid1_str()

        self.lock = threading.Lock()

        self.thread_max = thread_max
        self.current_thread_count = 0

    def _uuid1_str(self):
        '''Returns: random UUID tag '''
        return str(uuid.uuid1())

    def add_task(self, func, *args, **argv):
        '''Add task to Pool and wait to exec

        Params:
            func : A callable obj, the entity of the current task
            args : the args of [func]
            argv : the argv of [func]
        '''
        assert callable(func), '[!] Function can \'t be called'

        ret = {}
        ret['func'] = func
        ret['args'] = args
        ret['argv'] = argv
        ret['uuid'] = self.signal_name
        self.task_list.append(ret)

    def run(self):
        """"""
        Thread(target=self._run).start()

        return self.result_queue

    #----------------------------------------------------------------------
    def _run(self):
        """"""
        for i in self.task_list:
            #print self.current_thread_count
            while self.thread_max <= self.current_thread_count:
                time.sleep(0.3)
            self._start_task(i)        

    def _start_task(self, task):
        """"""
        self.current_thread_count = self.current_thread_count + 1
        try:

            Thread(target=self._worker, args=(task,)).start()
        except TypeError:
            self.current_thread_count = self.current_thread_count - 1

    def _worker(self, dictobj):
        """"""
        func = dictobj['func']
        args = dictobj['args']
        argv = dictobj['argv']

        result = func(*args, **argv)

        self.lock.acquire()
        self._add_result_to_queue(result=result)
        self.lock.release()

    def _add_result_to_queue(self, **kw):
        """"""
        assert kw.has_key('result'), '[!] Result Error!'

        self.result_queue.put(kw['result']) 
        self.current_thread_count = self.current_thread_count - 1


class UtilsTest(unittest.case.TestCase):
    def runTest(self):
        ms = inspect.getmembers(self)
        ms = map(lambda x: x[0], ms)
        for i in ms:
            if callable(getattr(self,i)):
                if i.startswith('test_'):
                    getattr(self, i)()    

    def test_pool(self):
        def demo_task(*args):
            '''simulate the plugin.run'''
            print '[!] Computing!'
            time.sleep(args[0])
            print '[!] Finished!'
            print
            returns = 'Runtime Length : %s' % str(args)
            return returns
        pool = Contractor()
        pool.add_task(demo_task, 7)
        pool.add_task(demo_task, 3)
        q = pool.run()
        print pool.current_thread_count
        self.assertIsInstance(q, Queue)

        r = q.get()
        print r
        self.assertIsInstance(r, str)
        r = q.get()
        print r
        self.assertIsInstance(r, str)

        print pool.current_thread_count


if __name__ == '__main__':
    unittest.main()