#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Parse dict
  Created: 2016/12/16
"""

import shelve
import unittest
import os
from pprint import pprint
from hashlib import md5

SESSION_TABLE_FILE = 'sessions_dat'
DEFAULT_SESSION_ID = 'default'

########################################################################
class DictParser(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, filename, 
                 session_id=SESSION_TABLE_FILE,
                 do_continue=False,
                 session_data_file=SESSION_TABLE_FILE):
        """Constructor
        
        Params:
            filename: :str: the target dict you want to use
            session_id: :str: the id you want to use to identify your session
            do_continue: :bool: continue or not
            session_data_file: :str: the file you want to save session info
            """
        abspathfile = os.path.abspath(filename)
        if os.path.exists(abspathfile):
            self._filename = filename
        else:
            raise Exception('[!] No Such Dict File')
        
        self._session_data_file = session_data_file
        self._session_id = md5(str(session_id+filename).encode('utf-8')).hexdigest()
        
        self._dict_file_p = open(self._filename)
        try:
            self._session_progress_table = shelve.open(os.path.abspath(self._session_data_file))
        except:
            os.remove(os.path.abspath(self._session_data_file))
            self._session_progress_table = shelve.open(os.path.abspath(self._session_data_file))
        # continue last task
        if do_continue:
            if self._session_id in self._session_progress_table:
                try:
                    pos = self._session_progress_table[self._session_id]
                except ValueError:
                    pos = 0
                self._dict_file_p.seek(pos)

    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        return self
        

    #----------------------------------------------------------------------
    def __next__(self):
        """"""
        return self._next()
    
    #----------------------------------------------------------------------
    def next(self):
        """"""
        return self._next()
        
    
    #----------------------------------------------------------------------
    def _next(self):
        """"""
        self._current_pos = 0
        self._current_pos = self._dict_file_p.tell()
        while True:
            ret = self._dict_file_p.readline()
            self.save()
            if ret.strip() == '':
                #_empty_lines_count = _empty_lines_count + 1
                if self._dict_file_p.tell() == self._current_pos:
                    raise StopIteration()
                else:
                    continue
            else:
                return ret.strip()
            
    #----------------------------------------------------------------------
    def save(self):
        """"""
        if self._current_pos - self._dict_file_p.tell() >= 1024:
            self._save()        
        #print self._session_progress_table
    
    
    #----------------------------------------------------------------------
    def _save(self):
        """Save the progress"""
        self._session_progress_table[self._session_id] = self._dict_file_p.tell()
     
    #----------------------------------------------------------------------
    def force_save(self):
        """Force save"""
        self._save()
        
    
    #----------------------------------------------------------------------
    def __del__(self):
        """Close the opened resource"""
        try:
            self._dict_file_p.close()
            self._session_progress_table.close()
        except AttributeError:
            pass
 
    #----------------------------------------------------------------------
    def get_next_collection(self, num=200):
        """Returns a tuple for the next [num] paylaod(lines)"""
        ret = []
        for i in range(num):
            try:
                ret.append(self._next())
            except StopIteration:
                pass
        self._save()
        
        return tuple(ret)
    
    #----------------------------------------------------------------------
    def get_current_pos(self):
        """The current pos"""
        return self._dict_file_p.tell()
    
    #----------------------------------------------------------------------
    def get_total_size(self):
        """total size(progress)"""
        return os.path.getsize(self._filename)
        
    #----------------------------------------------------------------------
    def get_fp(self):
        """Get the fp(Dangerous)"""
        return self._dict_file_p
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        self._dict_file_p.seek(0)
        
        
        

if __name__ == '__main__':
    unittest.main()