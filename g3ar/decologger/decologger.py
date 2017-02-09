#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Main Module for decologger
  Created: 2016/12/18
"""


import unittest
import logging
import time
import sys
import os
import traceback
import pprint
import json
from os.path import join as pathjoin
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
    
    
#----------------------------------------------------------------------
def get_date():
    """"""
    return time.strftime("%Y%m%d", time.localtime(time.time()))

#----------------------------------------------------------------------
def get_func_info(func):
    """"""
    assert callable(func)
    return '[Module:' + str(__package__) + '.'\
           +str(__name__) + ' FunctionName:' + func.__name__ + ']'
    

#----------------------------------------------------------------------
def get_log_formatter(rule):
    """"""
    return logging.Formatter(rule)
    

LOW_LEVEL_LOG_PARAMS = {
    "log_called":True,
    'log_trace':False,
    "log_exception":True,
    'log_notify_admin':False
}

MIDDLE_LEVEL_LOG_PARAMS = {
    "log_called":True,
    'log_trace':False,
    "log_exception":True,
    'log_notify_admin':False
}

HIGH_LEVEL_LOG_PARAMS = {
    "log_called":True,
    'log_trace':True,
    "log_exception":True,
    'log_notify_admin':True
}

DEFAULT_FORMATTER_RULE = '%(asctime)s-%(name)s-%(levelname)s:' + \
    ' %(message)s -- [process_id:%(process)s]' + \
    '[thread_name:%(threadName)s-id:%(thread)s]'


########################################################################
class Decologger(object):
    """"""
    

    #----------------------------------------------------------------------
    def __init__(self, name, root_log_level='warning', 
                 basedir='decolog/', email_config={},):
        """Constructor
        
        Params:
            name: :str: the name of decologger
            root_log_level: :str: root logger level [debug/info/warning/error/critical]
            basedir: :str: the base path for all logs
            email_config: :str: Not Finished (If the crucial event happend, email to admin)
        """
        self._name = name
        self._email_config = email_config
        # set basedir
        self._basedir = os.path.abspath(basedir)
        self._basedir = pathjoin(self._basedir, self._name + '/')
        if not os.path.exists(self._basedir):
            os.makedirs(self._basedir)
        
        #
        # init root logger
        #
        assert isinstance(self._name, str)
        self._root_logger = logging.getLogger(self._name)
        self._root_logger.setLevel(root_log_level.upper())
        
        root_logger_filehandler = logging.handlers.TimedRotatingFileHandler(
            filename=pathjoin(self._basedir, self._name + '.log'), 
            when='D'
        )
        root_logger_filehandler.setFormatter(get_log_formatter(DEFAULT_FORMATTER_RULE))
        
        stdouthandler = logging.StreamHandler(sys.stdout)
        stdouthandler.setFormatter(get_log_formatter(DEFAULT_FORMATTER_RULE))
        stderrhandler = logging.StreamHandler(sys.stderr)
        stderrhandler.setFormatter(get_log_formatter(DEFAULT_FORMATTER_RULE))
        
        self._root_logger.addHandler(root_logger_filehandler)
        self._root_logger.addHandler(stderrhandler)
        self._root_logger.addHandler(stdouthandler)
        
        #
        # Init sub logger
        #
        self._info = self._init_sub_logger('info')
        self._debug = self._init_sub_logger('debug')
        self._warning = self._init_sub_logger('warning')
        self._error = self._init_sub_logger('error')
        self._critical = self._init_sub_logger('critical')
        
        #
        # Init crucial logger
        #
        self._crucial_logger = self._init_sub_logger('crucial')
        
    #----------------------------------------------------------------------
    def _init_sub_logger(self, sub_logger_name):
        """"""
        level = sub_logger_name.upper()
        
        sublogger_fullname = self._name + '.' + sub_logger_name
        sublogger_filename = sublogger_fullname + '.log'
        sublogger_filename_full = pathjoin(self._basedir, sublogger_filename)
        
        filehandler = logging.handlers.TimedRotatingFileHandler(
            filename=sublogger_filename_full,
            when='D',        
        )
        filehandler.setFormatter(get_log_formatter(DEFAULT_FORMATTER_RULE))
        
        logger = logging.getLogger(sublogger_fullname)
        
        if level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            logger.setLevel(level)
        elif level == 'CRUCIAL':
            logger.setLevel('CRITICAL')
        else:
            pass
        
        logger.addHandler(filehandler)
        
        if sub_logger_name.upper() == "CRITICAL" or \
           sub_logger_name.upper() == 'CRUCIAL':
            if self._email_config == {}:
                pass
            else:
                NotImplemented('[!] Under constructed')
        elif sub_logger_name.upper() == 'ERROR':
            #
            # if neccessary, define it
            #
            pass
        
        return logger
    
    #----------------------------------------------------------------------
    @property    
    def name(self):
        """"""
        return self._name
    
    #----------------------------------------------------------------------
    def low_level(self, func):
        """"""
        return self.costom(**LOW_LEVEL_LOG_PARAMS)(func)
        
    #----------------------------------------------------------------------
    def middle_level(self, func):
        """"""
        return self.costom(**MIDDLE_LEVEL_LOG_PARAMS)(func)
        
    #----------------------------------------------------------------------
    def high_level(self, func):
        """"""
        return self.costom(**HIGH_LEVEL_LOG_PARAMS)(func)
        
    
    #----------------------------------------------------------------------
    def ordinary(self, func):
        """"""
        return self.costom(**LOW_LEVEL_LOG_PARAMS)(func)

    #----------------------------------------------------------------------
    def essential(self, func):
        """"""
        return self.costom(**MIDDLE_LEVEL_LOG_PARAMS)(func)
        
    #----------------------------------------------------------------------
    def crucial(self, func):
        """"""
        #print 'function recved'
        #print 'Crucial Called'
        return self.costom(**HIGH_LEVEL_LOG_PARAMS)(func)
    
    #----------------------------------------------------------------------
    def ordinary_dctr(self, func):
        """"""
        print('function recved')
        return func
        
    
    #----------------------------------------------------------------------
    def costom(self, log_called=True,
               log_trace=False,
               log_exception=True,
               log_notify_admin=False):
        """"""
        def _costom(func):
            @wraps(func)
            def __costom(*vargs, **kwargs):
                ret = None
                try:
                    
                    if log_trace:
                        self.debug(msg='Into: ' + get_func_info(func))
                    if log_called:
                        self.info(msg=get_func_info(func) + ' Be Called')
                        
                    ret = func(*vargs, **kwargs)
                    
                    if log_trace:
                        self.debug(msg='Out of: ' + get_func_info(func))
                except Exception as e:
                    if log_exception:
                        self.crucial_log(repr(traceback.print_exc()))
                    
                    if log_notify_admin:
                        ret = traceback.format_exc()
                        self.notify(ret)
                    raise e
                finally:
                    return ret
            return __costom
        
        return _costom
        

    #----------------------------------------------------------------------
    def notify_costom(self):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def info(self, msg):
        """"""
        self._info.info(msg)
    
    #----------------------------------------------------------------------
    def debug(self, msg):
        """"""
        self._debug.debug(msg)
        
    #----------------------------------------------------------------------
    def warning(self, msg):
        """"""
        self._warning.warning(msg)
        
    #----------------------------------------------------------------------
    def error(self, msg):
        """"""
        self._error.error(msg)
    
    #----------------------------------------------------------------------
    def crucial_log(self, msg):
        """"""
        self._crucial_logger.critical(msg)
        self._critical.critical(msg)
        
    #----------------------------------------------------------------------
    def critical(self, msg):
        """"""
        self._critical.critical(msg)
        
        
    #----------------------------------------------------------------------
    def notify(self, msg, output_console=True, use_email=False):
        """"""
        if use_email:
            raise NotImplemented()
        
        if output_console:
            pprint.pprint(msg)

    

if __name__ == '__main__':
    dclogger = Decologger(name='HelloDeco')
    
    #----------------------------------------------------------------------
    @dclogger.crucial
    def test():
        """"""
        print('testcalled')
        print('Success')
        return "Success"
    
    print(test())
    
        
    
    unittest.main()