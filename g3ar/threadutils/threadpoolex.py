#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ThreadPool From Twisted and Add Common Resource
  Created: 05/13/17
"""

from __future__ import unicode_literals

import uuid
import threading
import traceback
try:
    import queue
except:
    import Queue as queue
import time
import random

class LaborQuit(Exception):
    pass

_callback_chain_lock = threading.Lock()

########################################################################
class ThreadPoolXLabor(threading.Thread):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, debug=True, loop_interval=0.2):
        """Constructor"""
        threading.Thread.__init__(self, name=name)

        #
        # key flag
        #
        self.working = False
        self._debug = True
        self._waiting_quit = False

        #
        # cache flag
        #
        self._cb_cached = False
        self._ecb_cached = False

        #
        # fields
        #
        self.loop_interval = loop_interval

        #
        # private attributes
        #
        self._task_buffer = queue.Queue(1)
        self._callback_chains_ = []
        self._exception_handle_callback_chains = []

        self._cb_c_buffer = self._callback_chains_
        self._ehcb_c_buffer = self._exception_handle_callback_chains
        
        self._inuse = False

    #----------------------------------------------------------------------
    def run(self):
        """"""
        try:
            self._run()
        except LaborQuit as e:
            pass
        
        #print(self.name, 'exited!')

    #----------------------------------------------------------------------
    def _run(self):
        """"""
        self.working = True
        while self.working:
            #
            # if quit, before get task
            #
            if self._waiting_quit:
                if self._task_buffer.qsize() <= 0:
                    self._quit()
            #
            # get task from task_buffer
            # 
            _task = self._get_current_task()

            #
            # process _task
            #
            if _task:
                _callabled = _task[0]
                _vargs = _task[1]
                _kwargs = _task[2]

                #
                # define exception
                #
                exc = None
                try:
                    _result = _callabled(*_vargs, **_kwargs)
                    
                    self._handle_result(_result)


                    #
                    # recovery callback chains
                    #
                    if self._cb_cached:
                        self._recovery_cb_chain()
                        self._cb_cached = False
                except Exception as e:
                    
                    self._handle_exception(e)

                    #
                    # recovery error_callback 
                    #
                    if self._ecb_cached:
                        self._recovery_ecb_chain()
                        self._ecb_cached = False
                
                self.inuse = False

            else:
                if self._waiting_quit:
                    if self._task_buffer.qsize() == 0:
                        self._quit()
                time.sleep(self.loop_interval)

    #----------------------------------------------------------------------
    @property
    def busy(self):
        """"""
        if self._task_buffer.qsize() == 0:
            return False
        else:
            return True
    
    @property
    def inuse(self):
        """"""
        return self._inuse
    
    @inuse.setter
    def inuse(self, flag):
        """"""
        self._inuse = flag
        

    #----------------------------------------------------------------------
    def _handle_exception(self, exception_obj):
        """"""
        e = exception_obj
        #
        # exception callback
        #
        if self._exception_handle_callback_chains == []:
            if self._debug:
                raise e
        else:
            for i in self._exception_handle_callback_chains:
                e = i(e)
    
    @property
    def cb_chain(self):
        """"""
        #if isinstance(self._callback_chains_, list):
        return self._callback_chains_
        #else:
        #   return self._cb_c_buffer

    #----------------------------------------------------------------------
    def _handle_result(self, result):
        """"""
        _result = result

        #
        # process result callback
        #        
        _cs = self.cb_chain
        for i in _cs:

            _cb = i[0]
            _exc_cb = i[1]

            try:
                _result = _cb(_result)
            except Exception as e:
                #
                # if some exception happend
                #
                if _exc_cb:
                    _result = _exc_cb(_result)
                else:
                    raise e        


    #----------------------------------------------------------------------
    def _get_current_task(self):
        """"""
        try:
            _ret = self._task_buffer.get_nowait()
        except:
            _ret = None

        return _ret

    #----------------------------------------------------------------------
    def add_callback(self, callback, exception_callback=None):
        """result callback function"""
        assert callable(callback), 'callback cannot be called'

        self._callback_chains_.append((callback, exception_callback))

    #----------------------------------------------------------------------
    def add_task_exception_callback(self, callback):
        """"""
        assert callable(callback), 'exception callback'

        self._exception_handle_callback_chains.append(callback)


    #----------------------------------------------------------------------
    def _execute(self, target, var_args=tuple(), keyword_args={}):
        """"""
        assert callable(target), 'target function cannot be called'
        assert not self._waiting_quit, 'waiting for quiting, cannot execute task'

        self._task_buffer.put(tuple([target, var_args, keyword_args]))

    #----------------------------------------------------------------------
    def execute(self, target, var_args=tuple(), keyword_args={}):
        """"""
        if self._cb_cached:
            self._recovery_cb_chain()

        if self._ecb_cached:
            self._recovery_ecb_chain()

        self._execute(target, var_args, keyword_args)

    #----------------------------------------------------------------------
    def execute_with_callback(self, target, var_args=tuple(), keyword_args={},
                              callback=None, callback_exc=None, error_callback=None,):
        """"""
        assert callable(target), 'target function cannot be called'
        assert not self._waiting_quit, 'waiting for quiting, cannot execute task'

        #
        # process callback
        # 
        if callback:
            self._cache_cb_chain()
            self.add_callback(callback, callback_exc)

        if error_callback:
            self._cache_ecb_chain()
            self.add_task_exception_callback(error_callback)

        #
        # execute called
        #
        self._execute(target, var_args, keyword_args)
        
        self.quit()


    #----------------------------------------------------------------------
    def execute_with_callback_chains(self, target, var_args=tuple(), keyword_args={},
                                     callback_chain=None, error_callback_chains=None):
        """"""
        assert callable(target), 'target function cannot be called'
        assert not self._waiting_quit, 'waiting for quiting, cannot execute task'
        assert callback_chain == None or isinstance(callback_chain, list), \
               'callback chain has to be None or list'
        assert error_callback_chains == None or isinstance(error_callback_chains, list), \
               'callback chain has to be None or list'

        #
        # proccess callback
        #
        if callback_chain:
            self._cache_cb_chain()
            self._callback_chains_ = callback_chain

        if error_callback_chains:
            self._cache_ecb_chain()
            self._exception_handle_callback_chains = error_callback_chains

        self._execute(target, var_args, keyword_args)
        
        self.quit()

    #----------------------------------------------------------------------
    def _cache_cb_chain(self):
        """"""
        #
        # cache callback
        #
        self._cb_c_buffer = self._callback_chains_

        #
        # change flag
        #
        self._cb_cached = True

        #
        # reset chains
        #
        self._callback_chains_ = []

    #----------------------------------------------------------------------
    def _recovery_cb_chain(self):
        """"""
        self._cb_cached = False
        self._callback_chains_ = self._cb_c_buffer


    #----------------------------------------------------------------------
    def _recovery_ecb_chain(self):
        """"""
        self._ecb_cached = False
        self._exception_handle_callback_chains = self._cache_ecb_chain     

    #----------------------------------------------------------------------
    def _cache_ecb_chain(self):
        """The same as self._cache_cb_chain"""
        self._ehcb_c_buffer = self._exception_handle_callback_chains
        self._ecb_cached = True
        self._exception_handle_callback_chains = []


    #----------------------------------------------------------------------
    def quit(self):
        """"""
        self._waiting_quit = True

    #----------------------------------------------------------------------
    def _quit(self):
        """"""
        raise LaborQuit('normal exit labor')


########################################################################
class _LaborFactory(object):
    """"""
    count = 0
    Labor = ThreadPoolXLabor

    #----------------------------------------------------------------------
    def __init__(self, debug, loop_interval):
        """"""

        self._loop_interval = loop_interval
        self._debug = debug

        self._callback_chains = []
        self._exception_callback_chains = []

    #----------------------------------------------------------------------
    def add_callbacks(self, callback, callback_exc=None):
        """"""
        assert callable(callback), 'callback not callable'
        assert callback_exc == None or callable(callback_exc), 'result exception callback not callable.'

        self._callback_chains.append(tuple([callback, callback_exc]))

    #----------------------------------------------------------------------
    def add_callback_chain(self, callback_chain):
        """"""
        assert isinstance(callback_chain, list), 'callback chain must be list'
        self._callback_chains = callback_chain

    #----------------------------------------------------------------------
    def add_exception_callback(self, callback):
        """"""
        assert callable(callback), 'exception callback cannot be called'

        self._exception_callback_chains.append(callback)

    #----------------------------------------------------------------------
    def add_exception_callback_chain(self, callback_chain):
        """"""
        assert isinstance(callback_chain, list), 'callback chain must be list'

        self._exception_callback_chains = callback_chain

    @property
    def callback_chains(self):
        """"""
        return self._callback_chains
    
    @property
    def exception_callback_chains(self):
        """"""
        return self._exception_callback_chains

    #----------------------------------------------------------------------
    def build_labor(self):
        """"""

        _lb = self.Labor(name=self.gen_labor_name(), 
                         debug=self._debug, 
                         loop_interval=self._loop_interval)
        _lb.daemon = True

        #
        # add result callback
        #
        for i in self.callback_chains:
            _lb.add_callback(*i)

        #
        # add exception callback
        #
        for i in self.exception_callback_chains:
            _lb.add_task_exception_callback(i)

        return _lb

    #----------------------------------------------------------------------
    def gen_labor_name(self):
        """"""
        return 'labor-starttime:{ts}'.format(index=self.count, 
                                                     ts=int(time.time()*100))






########################################################################
class _ThreadTeam(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, factory):
        """Constructor"""
        assert isinstance(factory, _LaborFactory)

        self._factory = factory

        self._labors = []

    #----------------------------------------------------------------------
    @property    
    def labors(self):
        """"""
        return self._labors

    #----------------------------------------------------------------------
    def add(self):
        """"""
        lb = self._factory.build_labor()
        #
        # start labor
        #
        lb.daemon = True
        lb.start()
        self.labors.append(lb)
        return lb

    #----------------------------------------------------------------------
    def shrink(self):
        """"""
        #
        # shrink
        #
        map(self._exit_idle_labor, self.labors)

    #----------------------------------------------------------------------
    def _exit_idle_labor(self, labor):
        """"""
        assert isinstance(labor, ThreadPoolXLabor)

        if labor.is_alive():
            if labor.busy:
                pass
            else:
                self.labors.remove(labor)
                labor.quit()
        else:
            self.labors.remove(labor)

    #----------------------------------------------------------------------
    @property
    def size(self):
        """"""
        return len(filter(lambda x: x.is_alive(), self.labors))

    #----------------------------------------------------------------------
    def quitall(self):
        """"""
        #
        # shrink first
        #
        self.shrink()

        #
        # quit all labor
        #
        for i in self.labors:
            i.quit()
            try:
                i.join()
            except:
                pass
            
            while i.is_alive():
                pass

    #----------------------------------------------------------------------
    def select(self):
        """"""
        _idle_labors = filter(lambda x: not x.inuse, self.labors)

        if _idle_labors == []:
            return None
        else:
            
            labor = random.choice(_idle_labors)
            labor.inuse = True
            #while labor in self._selected_labor:
                #labor = random.choice(_idle_labors)

            #self._selected_labor_lock.acquire()
            #if labor in self._selected_labor:
                #pass
            #else:
                #self._selected_labor.append(labor)
            #self._selected_labor_lock.release()
            return labor

    #----------------------------------------------------------------------
    def release_labor(self, labor):
        """"""
        #
        # sync selected labor
        #
        #self._selected_labor_lock.acquire()
        #self._selected_labor.remove(labor)
        #self._selected_labor_lock.release()



########################################################################
class ThreadPoolX(object):
    """"""

    min_size = 5
    max_size = 20

    joined = False
    started = False

    workers = 0
    name = 'default'

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, 
                 name='default', debug=True, loop_interval=0.2,
                 adjuest_interval=3, diviation_ms=100):
        """Create threadpool object

        @param min_threads: min size of thread pool
        @type min_threads: L{int}

        @param max_threads: max size of thread pool
        @type max_threads: L{int}

        @param name: The name to give this threadpool; visible in log msg.
        @type name: native L{str}"""

        assert min_threads >= 0, 'minimum is negative'
        assert min_threads <= max_threads, 'maximum is less than minimum'

        self.min_size = min_threads
        self.max_size = max_threads

        self.name = name
        self.diviation_ms = diviation_ms
        #self.threads = []

        #
        # init factory
        #
        self._factory = _LaborFactory(debug, loop_interval)

        #
        # init _team
        #
        self._team = _ThreadTeam(self._factory)

        #
        # private entity
        #
        self._task_queue = queue.Queue()

        #
        # control adjust pool size interval
        #
        self._lp_itrvl = loop_interval
        self._adj_itrvl = adjuest_interval

        #
        # dispatcher
        #
        def _dispatcher_factory():
            _ret =  threading.Thread(name='ThreadPoolX:{name} Dispatcher'\
                                     .format(name=self.name), 
                                     target=self._start)

            _ret.daemon = True
            return _ret

        self._dispatcher = _dispatcher_factory()
        
        
        self._temp_factory = _LaborFactory(debug, loop_interval)

    #
    # set callback
    #
    #----------------------------------------------------------------------
    def add_callbacks(self, callback, callback_exc=None):
        """"""
        self._factory.add_callbacks(callback, callback_exc)

    #----------------------------------------------------------------------
    def add_callback_chain(self, callback_chain):
        """"""
        self._factory.add_callback_chain(callback_chain)

    #----------------------------------------------------------------------
    def add_exception_callback(self, callback):
        """"""
        self._factory.add_exception_callback(callback)

    #----------------------------------------------------------------------
    def add_exception_callback_chain(self, callback_chain):
        """"""
        self._factory.add_exception_callback_chain(callback_chain)

    #----------------------------------------------------------------------
    def _start(self):
        """"""
        self.started = True
        self.adjust_pool_size()
        while self.started:
            if int(int(time.time()*1000000) % (self._adj_itrvl*1000000)) <= self.diviation_ms:
                #print 'adpool'

                self.adjust_pool_size()
            #print self.dumped_status()
            #
            # consume task
            #
            self.consume()
            #

    #----------------------------------------------------------------------
    def start(self):
        """"""
        self._dispatcher.start()

    #----------------------------------------------------------------------
    def join(self):
        """"""
        self._dispatcher.join()

    #----------------------------------------------------------------------
    def quit(self):
        """"""
        self.started = False
        #self.join()
        while self._dispatcher.is_alive():
            pass
        print('Existed ThreadPool MainLoop(Dispatcher!)')
        self._team.quitall()
        print('Quit All Labor!')


    #----------------------------------------------------------------------
    def dumped_status(self):
        """"""
        state = {}
        state['name'] = self.name
        state['current_size'] = self._team.size
        state['idle_labor_size'] = len(filter(lambda x: x.is_alive() and not x.busy, self._team.labors))

        return state


    #----------------------------------------------------------------------
    def consume(self):
        """"""
        #
        # check team and select a idle labor
        #
        _labor = self._team.select()

        if _labor:
            pass
        else:
            if self._team.size < self.max_size:
                self._team.add() 
                _labor = self._team.select()
            else:
                _labor = None

        #
        # labor existed, execute task
        #
        if _labor:
            try:
                _task = self._task_queue.get_nowait()
            except queue.Empty:
                _task = None

            if _task != None:
                #print("******")
                _labor.execute(*_task)
            else:
                _labor.inuse = False

            #self._team.release_labor(_labor)
        else:
            pass

    #----------------------------------------------------------------------
    def adjust_pool_size(self):
        """"""

        while self._team.size < self.min_size:
            self._team.add()

        if self._team.size > self.max_size:
            self._team.shrink()

    #----------------------------------------------------------------------
    def feed(self, target, vargs=tuple(), kwargs={}):
        """"""
        assert callable(target), 'target function cannot be executed'

        self._task_queue.put(tuple([target, vargs, kwargs]))

    #----------------------------------------------------------------------
    def feed_with_callback(self, target, vargs=tuple(), kwargs={}, 
                           callback=None, callback_exc=None, error_callback=None):
        """"""
        assert callable(target), 'target function cannot be executed'

        _temp_labor = self._temp_factory.build_labor()
        _temp_labor.execute_with_callback(target, vargs, kwargs, callback,
                                          callback_exc, error_callback)
        _temp_labor.start()

    #----------------------------------------------------------------------
    def feed_with_callback_chain(self, target, vargs=tuple(), kwargs={},
                                 callback_chain=None, error_callback_chain=None):
        """"""
        assert callable(target), 'target function cannot be executed'

        _temp_labor = self._temp_factory.build_labor()
        _temp_labor.execute_with_callback_chains(target, vargs, kwargs,
                                                 callback_chain=callback_chain, 
                                                 error_callback_chains=error_callback_chain)
        _temp_labor.start()

 