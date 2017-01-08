#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar Test
  Created: 2016/12/23
"""
import sys
sys.path.append('..')

import unittest
import traceback

from time import sleep
#from g3ar.threadutils import thread_pool, contractor
#from g3ar.taskbulter import task_bulter
try:
    from Queue import Empty, Queue
except:
    from queue import Empty, Queue
#ThreadPool = thread_pool.Pool
#Contractor = contractor.Contractor
#TaskBulter = task_bulter.TaskBulter
from g3ar import TaskBulter
from g3ar import Contractor
from g3ar import TaskBulter
from g3ar import ThreadPool
from g3ar import DecoLogger
from g3ar.dict_parser import *
from g3ar.utils.import_utils import *
from g3ar.utils.inspect_utils import *
#from g3ar.utils.ip_calc_utils import *
from g3ar.utils.print_utils import *
from g3ar.utils.queue_utils import *
from g3ar import dict_parser
from g3ar.utils import ip_calc_utils, queue_utils

Decologger = DecoLogger

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
            print(pool.task_count)
            print(pool.executed_task_count)
            print(pool.percent)
            print(i)


        for i in range(21,41):
            pool.feed(testthreadpool_function, arg1=i)


        result_queue = pool.get_result_queue()

        while True:
            try:
                print(result_queue.get(timeout=2))
            except Empty:
                print('End!')
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
            print(i)

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
                print(result_queue.get(timeout=2))
            except Empty:
                print('End!')
                break




########################################################################
class G3arTaskBulterTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_taskbulter(self):
        """Constructor"""
        bulter = TaskBulter()
        bulter.start_task(id='tasktest', target=tasktest, args=(5,))
        task = bulter.get_task_by_id('tasktest')
        print(task)
        sleep(2)
        print(bulter.get_tasks_status())
        bulter.destory_task(task)
        #bulter.close()

########################################################################
class DictParserTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_dict_basic_api(self):
        """Constructor"""
        pprint('='*64)
        pprint('Test Dict Parser Parse A Small Dictionary')
        dictparse = DictParser(filename='testdata/dir.txt', do_continue=False)
        
        count = 0
        for i in dictparse:
            pprint(i)
            count = count + 1
            if count > 10:
                break
            
        dictparse = DictParser(filename='testdata/dir.txt', do_continue=True)
        retcollect = dictparse.get_next_collection(num=200)
        
        for i in retcollect:
            pprint(i)
        pprint('='*64)
    
    #----------------------------------------------------------------------
    def test_get_an_collection(self):
        """"""
        
        pprint('='*64)
        pprint('Test get a collection by dictparser')
        dictparse = DictParser(filename='testdata/dir.txt', do_continue=False)
        retcollect = dictparse.get_next_collection(num=200)
        
        for i in retcollect:
            pprint(i)
        pprint('='*64)
        
    #----------------------------------------------------------------------
    def test_get_basic_information(self):
        """"""
        pprint('='*64)
        pprint('Test get basic information of dictfile')
        dictparse = DictParser(filename='testdata/dir.txt', do_continue=False)
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())
        dictparse.get_fp().readline()
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())  
        #dictparse.reset()
        dictparse.get_fp().readline()
        pprint("Current Pos: %d" % dictparse.get_current_pos())
        pprint("Totol SIZE: %d" % dictparse.get_total_size())        
        pprint('='*64)

########################################################################
class PrintBarTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        print_bar('WellCome TO MY G3ar')
        print_bar(basic_char='0')
        print_bar(color='red')
    
########################################################################
class InspectUtilsTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""
        ret = get_args_dict(ip_calc_utils.ip2int)
        pprint(ret)
        ret = get_neccessary_params(ip_calc_utils.ipv4_range)
        pprint(ret)        
        ret = get_callables(ip_calc_utils)
        pprint(ret)
        ret = get_fileds(ip_calc_utils)
        pprint(ret)
        ret = get_methods(ip_calc_utils)
        pprint(ret)
        ret = get_functions(ip_calc_utils)
        pprint(ret)  
        
########################################################################
    
    
########################################################################
class QueueUtilsTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_queue_dispatcher(self):
        """"""
        task_q = Queue()
        queue_utils.async_dispatch(task_q, (x for x in range(365)))
        for i in range(300):
            print(task_q.get())

########################################################################
class DecologgerTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_learn_decorector(self):
        """"""
        print(('='*64))
        def logit(func):
            def wrapper(*args, **kwargs):
                print(('wrapper got param', args, kwargs))
                print(('pre call', func.__name__))
                return func(*args, **kwargs)
            return wrapper
    
        #----------------------------------------------------------------------
        @logit
        def funct(args):
            """"""
            print(('funct called! Got Param', args))
        
        funct('Hello')
        
        def sss(*arg):
            print(arg)
            print('sssss called') 
            return logit(arg[0])
        
        @sss
        def tests():
            print('tests called')
        
        tests()
        
        print(('='*64))
    
    def test_exception(self):
        try:
            raise Exception('adfasdfasdf')
        except:
            print(traceback.extract_stack())
            traceback.format_exc()
    
    #----------------------------------------------------------------------
    def test_decologger_basic_api(self):
        """"""
        dclogger = Decologger(name='testlogger', basedir='testdata/decolog/')
        
        
        class A(object):
            #----------------------------------------------------------------------
            def __init__(self):
                """"""
                pass
            
            #----------------------------------------------------------------------
            @dclogger.crucial
            def B(self):
                """"""
                print('B Called!')
        
        
        dclogger.critical('Hello Critical')
        A().B()
                
        
        print(('='*64))
        
        
        
    
            
if __name__ == '__main__':
    unittest.main()
