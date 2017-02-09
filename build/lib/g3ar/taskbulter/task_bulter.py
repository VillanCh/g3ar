#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Manage Task
  Created: 2016/12/13
"""

from time import sleep
import unittest
from multiprocessing import Pipe
from threading import Thread
from pprint import pprint
from inspect import getmembers

from . import exceptions
from .process_task import ProcessTask
from .utils_class import Singleton
from .process_task import testfun



UPDATE_TASK_STATUS_DAEMON = 'update_task_status_daemon'


########################################################################
class TaskBulter(Singleton):
    """"""

    _tasks_table = {}
    _tasks_status = {}
    _daemon_threads = {}
    _result_tables = {}
    
    #----------------------------------------------------------------------
    def __init__(self, threads_update_interval=0):
        """Constructor"""
        
        self._threads_update_interval = threads_update_interval
        self._closed = False
        self._initial_deamon_threads()
    
    #----------------------------------------------------------------------
    def _daemon_start(self, name, func):
        """"""
        if name in self._daemon_threads:
            pass
        else:
            ret = Thread(name=name, target=func)
            ret.daemon = True
            ret.start()
            self._daemon_threads[name] = ret

    #----------------------------------------------------------------------
    def _initial_deamon_threads(self):
        """"""
        #raise NotImplemented
    
        self._daemon_start(name=UPDATE_TASK_STATUS_DAEMON,
                     func=self._update_tasks_status)
        
    
    #----------------------------------------------------------------------
    def _update_tasks_status(self):
        """"""
        #pprint('daemon threads started')
        while self._closed == False:
            for i in list(self._tasks_table.items()):
                pipe = i[1]['status_monitor_pipe']
                if self._tasks_table[i[0]]['process_instance'].exitcode == None:
                    if pipe.poll():
                        self._tasks_status[i[0]] = pipe.recv()
                        #pprint(self._tasks_status)
                    else:
                        pass
                    sleep(self._threads_update_interval/2)
                else:
                    self._tasks_status[i[0]] = {}
    
    
    #----------------------------------------------------------------------
    def start_task(cls, id, target, args=tuple(), kwargs={}, result_callback=None):
        """Start A task(Process)
        
        Params:
            id: the ID of task (identify the process_task)
              :type: str
            target: the task function
              :type: function
            args: the vargs of target
              :type: tuple
            kwargs: the keywords of target
              :type: dict"""
        
        if not callable(target): exceptions.TaskCannotBeCalled
        
        if id in cls._tasks_table:
            raise exceptions.ExistedTaskId
        
        #
        # create pipe
        #
        control_pipe, child_pipe = Pipe(duplex=False)
        result_recv_pipe, result_send_pipe = Pipe(duplex=False)
        
        #
        # init tables
        #
        cls._tasks_table[id] = {}
        cls._tasks_table[id]['status_monitor_pipe'] = control_pipe
        cls._result_tables[id]['result_pipe'] = result_recv_pipe
        
        #
        # Build process and run
        #
        task_process = ProcessTask(id, target, args=args, kwargs=kwargs, 
                                   status_monitor_pipe=child_pipe, 
                                   threads_update_interval=cls._threads_update_interval,
                                   result_pipe=result_send_pipe, result_hook_function=result_callback)
        
        cls._tasks_table[id]['process_instance'] = task_process
        task_process.daemon = True
        task_process.start()
    
    
    #----------------------------------------------------------------------
    def get_tasks_status(self):
        """"""
        return self._tasks_status.copy()
    
    #----------------------------------------------------------------------
    def get_tasks(self):
        """"""
        return self._tasks_table
    
    #----------------------------------------------------------------------
    def get_task_by_id(self, id):
        """"""
        if id in self._tasks_table:
            return self._tasks_table[id]
        else:
            return None
    
    #----------------------------------------------------------------------
    def destory_task(self, id_or_taskinstance):
        """"""
        if isinstance(id_or_taskinstance, ProcessTask):
            id_or_taskinstance.terminate()
        elif isinstance(id_or_taskinstance, str):
            _ = self.get_task_by_id(id_or_taskinstance)['process_instance']
            assert isinstance(_, ProcessTask)
            _.terminate()
        
    
    #----------------------------------------------------------------------
    def get_result_pipe_table(self):
        """"""
        return self._result_tables
            
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self._closed = True
        
########################################################################
class TaskBulterTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_add_task_and_kill_task(self):
        """Constructor"""
        TaskBulter().start_task(id='test-1', target=testfun, args=(6,))
        #sleep(1)
        for i in range(3):
            pprint(TaskBulter().get_task_status())
            
            self.assertIsInstance(TaskBulter().get_task_by_id('test-1')['process_instance'], ProcessTask)
            processi = TaskBulter().get_task_by_id('test-1')['process_instance']
            sleep(1)
        
        TaskBulter().start_task(id='test-2', target=testfun, args=(6,))
        processi = TaskBulter().get_task_by_id('test-2')['process_instance']
        #processi.terminate()
        TaskBulter().destory_task('test-2')
        
        for i in range(3):
            pprint(TaskBulter().get_task_status())
            self.assertIsInstance(TaskBulter().get_task_by_id('test-2')['process_instance'], ProcessTask)
            sleep(1)        
    
    


if __name__ == '__main__':
    unittest.main()