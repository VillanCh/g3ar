#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: process_task for a task(ProcessMode)
  Created: 2016/12/12
"""

import unittest
import time
import multiprocessing
import threading
from multiprocessing import Pipe
from pprint import pprint

import exceptions

def sleep_(num):
    #pprint("~~~")
    time.sleep(num)

#----------------------------------------------------------------------
def testfun(num):
    """"""
    #print('UserFunc called!')
    for i in range(6):
        threading.Thread(target=sleep_, args=(num,)).start()
        #print('SubProcess Called!')
    
    time.sleep(0.4)
    
    #pprint(threading.enumerate())

########################################################################
class ProcessTask(multiprocessing.Process):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target, args=tuple(), kwargs={}, status_monitor_pipe=None,
                 threads_update_interval=0.0):
        """Constructor"""
        
        multiprocessing.Process.__init__(self, name=id)
        
        self._target = target
        self.args = args
        self.kwargs = kwargs
        
        self._id = id
        
        self._sub_threads_list = []
    
        self._threads_update_interval = threads_update_interval
                
        self._status_monitor_pipe = status_monitor_pipe
        #self._init_timer()
    
    #----------------------------------------------------------------------
    def _init_timer(self):
        """"""
        self._threads_monitor = threading.Thread(name='update_subthreads_list',
                                                 target=self._deamon_check_threads)
        self._threads_monitor.daemon = True
        self._threads_monitor.start()
        
    
    #----------------------------------------------------------------------
    @property    
    def task_id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def run(self):
        """"""
        self._init_timer()
        try:
            self._target(*self.args, **self.kwargs)
        except exceptions.TaskRuntimeError:
            raise NotImplemented
        
    #----------------------------------------------------------------------
    def _enum_threads(self):
        """"""
        threads_list = threading.enumerate()
        return threads_list
    
    #----------------------------------------------------------------------
    def _deamon_check_threads(self):
        """"""
        assert isinstance(self._threads_update_interval, (int, float))
        while True:
            #pprint('test')
            
            self._sub_threads_list = None
            self._sub_threads_list = self._enum_threads()
            #print(len(self._sub_threads_list))
            #print len(self._sub_threads_list)
            threads_check_result = {}
            threads_check_result['from'] = self._id
            for i in self._sub_threads_list:
                threads_check_result[i.name] = i.is_alive()
                #pprint(threads_check_result)
                
            self._status_monitor_pipe.send(threads_check_result)
            time.sleep(self._threads_update_interval)
            
    ##----------------------------------------------------------------------
    #@property    
    #def subthreads_count(self):
        #return len(self._sub_threads_list)
        
            
        

########################################################################
class ProcessTaskTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def print_bar(self):
        """"""
        print('-'*64)
    
    #----------------------------------------------------------------------
    def print_end_bar(self):
        """"""
        print('-'*30 + 'END' + '-'*31)
        
        

    #----------------------------------------------------------------------
    def runTest(self):
        """"""
        pipp, pipc = Pipe()
        self.print_bar()
        print('Test Task Interface')
        ret_process = ProcessTask(id='test-1', target=testfun, args=(5,), 
                                  status_monitor_pipe=pipc)
        ret_process.start()
        print('Test get threads status')
        time.sleep(1)
        #print(ret_process.subthreads_count)
        
        
        threads_status = pipp.recv()
        self.assertIsInstance(threads_status, dict)
        self.print_end_bar()
        
        
    
    
        
if __name__ == '__main__':
    unittest.main()