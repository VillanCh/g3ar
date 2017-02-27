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
try:
    from Queue import Full, Empty, Queue
except:
    from queue import Full, Empty, Queue
#from random import choice
#from traceback import format_exc
from threading import Thread, Lock
#from multiprocessing import Process, Lock
from uuid import uuid1


########################################################################
class TaskError(Exception):
    """"""
    pass

########################################################################
class LaborThread(Thread):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, result_queue, master, clean_mod=True, *args, **kargs):
        """Constructor"""
        Thread.__init__(self, name='ThreadPool-Labor-'+uuid1().hex,
                        *args, **kargs)

        self._master = master

        self._clean_mod = clean_mod

        self._result_queue = result_queue

        self._startworkingflag_ = True

        self._task_queue = Queue(1)

        self._count_lock = Lock()

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
                    #self._result_queue.put(result)
                except Exception as e:
                    result['state'] = False
                    result['result'] = None
                    exception_i = (str(type(e)), str(e))
                    result['exception'] = exception_i
                finally:
                    if self._clean_mod:
                        _result = {}
                        _result['state'] = result['state']
                        _result['result'] = result['result']
                        result = _result
                    self._result_queue.put(result)

                self._count_lock.acquire()
                self._master._executed_task_count = \
                    self._master._executed_task_count + 1
                self._count_lock.release()
            except Empty:
                pass

    #----------------------------------------------------------------------
    def _process_task(self, task):
        """"""
        try:
            ret = task[0](*task[1], **task[2])
            return ret
        except Exception as e:
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
    def __init__(self, thread_max=30, clean_mod=True):
        """Constructor"""
        self.thread_max = thread_max

        self._current_thread = []
        self._daemon_thread = []
        self._clean_mod = clean_mod
        self._result_queue = Queue()

        self._task_queue = Queue()

        self.is_alive = True

        self._executed_task_count = 0
        self._task_count = 0

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
        _tmp_labor = LaborThread(result_queue=self._result_queue, master=self,
                                 clean_mod=self._clean_mod)
        _tmp_labor.daemon = True
        _tmp_labor.start()
        self._current_thread.append(_tmp_labor)

    #----------------------------------------------------------------------
    def feed(self, target_func, *vargs, **kwargs):
        """"""
        self._task_queue.put(tuple([target_func, vargs, kwargs]))
        self._task_count = self._task_count + 1

    #----------------------------------------------------------------------
    def _dispatcher(self):
        """"""
        #pprint('dispatcher start!')
        while self.is_alive:
            try:
                ret = self._task_queue.get()
                while True:
                    availible_threads = [None if x.get_task_queue().full() \
                                         else x for x in self._current_thread]
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

    #----------------------------------------------------------------------
    def get_result_generator(self):
        """"""
        while True:
            try:
                ret = self._result_queue.get(timeout=1)
                yield ret
            except Empty:
                if self._task_count == self._executed_task_count:
                    break
                else:
                    pass

    #----------------------------------------------------------------------
    @property
    def task_count(self):
        """The amount of tasks"""
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
        return float(self._executed_task_count)/float(self._task_count)
                


########################################################################
class PoolTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        self.test_laborprocess()

    #----------------------------------------------------------------------
    def test_pool(self):
        """"""
        def func1(arg1):
            print('func1 called!')
            return arg1

        pool = Pool()
        pool.start()
        pool.feed(func1, 12345)
        for i in range(10):
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
