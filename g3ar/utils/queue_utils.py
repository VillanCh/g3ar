#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Queue Utils
  Created: 2017/1/3
"""

import unittest
import threading
import time
try:
    from queue import Empty
except:
    from Queue import Empty
    
#----------------------------------------------------------------------
def sync_dispatch(queue_instance, task_generator, 
                  buffer_size=100, interval=0.05):
    """To dispatch tasks from [task_generator] to [queue_instance] 
    with the [buffer_size] buffer task.
    
    Params:
        queue_instance: :Queue: receive task.
        task_generator: :generator/list/tuple/set: Who have tasks 
            waiting for being dispatched.
        buffer_size: :int: buffer_size.
        interval: :float/int: interval of checking the size of queue."""
    
    assert isinstance(interval, (int, float)), \
           '[!] [interval] should be a float/int! '
    assert isinstance(buffer_size, int), \
           '[!] [buffer_size] should be a int! '
    
    for i in task_generator:
        while queue_instance.qsize() >= buffer_size:
            time.sleep(interval)
        queue_instance.put(i)

#----------------------------------------------------------------------
def async_dispatch(queue_instance, task_generator, 
                  buffer_size=100, interval=0.05,
                  thread_name='ASYNC_DISPATCHER', daemon=True):
    """To dispatch tasks from [task_generator] to [queue_instance] 
    with the [buffer_size] buffer task.
    
    Params:
        queue_instance: :Queue: receive task.
        task_generator: :generator/list/tuple/set: Who have tasks 
            waiting for being dispatched.
        buffer_size: :int: buffer_size
        interval: :float/int: interval of checking the size of queue.
        thread_name: :str: the name of thread.
        daemon: :bool: daemon thread?"""
    
    assert isinstance(interval, (int, float)), \
           '[!] [interval] should be a float/int! '
    assert isinstance(buffer_size, int), \
           '[!] [buffer_size] should be a int! '
    
    def _worker():
        for i in task_generator:
            while queue_instance.qsize() >= buffer_size:
                time.sleep(interval)
            queue_instance.put(i)
    
    _threadi = threading.Thread(name=thread_name, target=_worker)
    _threadi.daemon = True
    _threadi.start()
    
#----------------------------------------------------------------------
def queue_peek(queue_instance, timeout=60):
    """Convert Queue to A generator with a timeout
    
    Params:
        queue_instance: :Queue: the Queue you want to peek
        timeout: :int/float: from got a """
    while True:
        try:
            yield queue_instance.get(timeout=timeout)
        except Empty:
            break
    

if __name__ == '__main__':
    unittest.main()