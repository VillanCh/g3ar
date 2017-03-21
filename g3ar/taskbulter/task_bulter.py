#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Manage Task
  Created: 2016/12/13
"""

import time
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
        #self._initial_deamon_threads()
    
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

    ##----------------------------------------------------------------------
    #def _initial_deamon_threads(self):
        #""""""
        ##raise NotImplemented
    
        #self._daemon_start(name=UPDATE_TASK_STATUS_DAEMON,
                     #func=self._update_tasks_status)
        
    #----------------------------------------------------------------------
    def _upload_result_table(self):
        """"""
        taskslist = self._result_tables.keys()
        for task_id in taskslist:
            self.get_result(task_id)
        
    #----------------------------------------------------------------------
    def _update_tasks_status(self):
        """"""
        re_update = False
        for i in self._tasks_table.items():
            pipe = i[1]['status_monitor_pipe']
            #if self._tasks_table[i[0]]['process_instance'].exitcode == None:
            last = {}
            ret = {}
            while pipe.poll():
                ret = pipe.recv()
                #ret['timestamp'] = time.time()
            if ret != {}:
                pass
            else:
                ret = {}
            
            if not self._tasks_status[i[0]]:
                self._tasks_status[i[0]] = {}
            
            #
            # Clean last buffer record
            #
            _ = self._tasks_status[i[0]].copy()
            try:
                del _['last']
            except KeyError:
                pass
            last = _
            
            #
            # record 
            #
            self._tasks_status[i[0]]['now'] = ret
            if isinstance(self._tasks_status[i[0]], dict):
                self._tasks_status[i[0]]['last'] = last
            #else:
            #    pass
            
            #
            # Check Re-update?
            #
            try:
                lasttimestamp = int(self._tasks_status[i[0]]['now']['timestamp'])
            except KeyError:
                lasttimestamp = int(time.time())
                
            if int(time.time()) - \
               lasttimestamp \
               <= 3:
                re_update = False
            else:
                re_update = True
        
        if re_update:
            self._update_tasks_status()
    
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
        cls._result_tables[id] = {}
        cls._tasks_status[id] = {}
        
        cls._tasks_table[id]['status_monitor_pipe'] = control_pipe
        cls._result_tables[id]['result_pipe'] = result_recv_pipe
        cls._result_tables[id]['result'] = []
        
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
        self._update_tasks_status()
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
    def get_result(self, task_id):
        """"""
        resultset = self._result_tables.get(task_id)
        if resultset:
            pipe = resultset.get('result_pipe')
            if pipe:
                while pipe.poll():
                    resultset['result'].append(pipe.recv())
        
        return resultset.get('result')
        
    
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
    
    #----------------------------------------------------------------------
    def destory_and_clean_task(self, id):
        """"""
        tasklist = []
        if id:
            if id in self._tasks_table.keys():
                tasklist.append(id)
            else:
                return False
        else:
            tasklist = self._tasks_table.keys()
        
        for i in tasklist:
            self.destory_task(tasklist)
            del self._tasks_status[i]
            del self._tasks_table[i]
            del self._result_tables[i]
        
        return True
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        return self.destory_and_clean_task(None)

        
########################################################################
class TaskBulterTest(unittest.case.TestCase):
    """"""      
    
    #----------------------------------------------------------------------
    def test_get_result(self):
        """"""
        TaskBulter().start_task('testresultrecv', result_t)
        sleep(1)
        pprint(TaskBulter().get_result('testresultrecv'))

#----------------------------------------------------------------------
def result_t():
    """"""
    for i in range(6):
        yield i
    

if __name__ == '__main__':
    unittest.main()