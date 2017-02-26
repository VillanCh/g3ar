#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Parse dict
  Created: 2016/12/16
"""

import pickle
import unittest
import os
from codecs import open
from pprint import pprint
from hashlib import md5

SESSION_TABLE_FILE = 'sessions_dat'
DEFAULT_SESSION_ID = 'default'

#----------------------------------------------------------------------
def get_buffer(shelvefile, key=None):
    """"""
    if os.path.exists(shelvefile):
        pass
    else:
        if key:
            set_buffer(shelvefile, key, value=0)
        else:
            set_buffer(shelvefile, key='default', value=0)
    
    with open(shelvefile, 'rb',) as fp:
        try:
            text = fp.read()
            pdict = pickle.loads(text)
            assert isinstance(pdict, dict)
            if key:
                result = pdict.get(key)
            else:
                result = pdict            
        except:
            if key:
                
                result = None
            else:
                result = {}


    
    return result


#----------------------------------------------------------------------
def set_buffer(shelvefile, key, value):
    """"""
    if os.path.exists(shelvefile):
        pdict = get_buffer(shelvefile)
    else:
        pdict = {}
    
    pdict[key] = value
    text = pickle.dumps(pdict)
    
    with open(shelvefile, 'wb') as fp:
        fp.write(text)





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

        try:
            self._session_progress_table = get_buffer(self._session_data_file)
        except:
            os.remove(os.path.abspath(self._session_data_file))
            self._session_progress_table = get_buffer(self._session_data_file)

        self._do_continue = do_continue

        if hasattr(self, '_dict_file_p'):
            pass
        else:
            self.__enter__()
                
    #----------------------------------------------------------------------
    def __enter__(self):
        """"""
        self._dict_file_p = open(self._filename)
        
        # continue last task
        if self._do_continue:
            if self._session_id in self._session_progress_table:
                try:
                    pos = get_buffer(self._session_data_file, self._session_id)
                except ValueError:
                    pos = 0
                self._dict_file_p.seek(pos)      
                
        return self
    
    #----------------------------------------------------------------------
    def __exit__(self):
        """"""
        self._dict_file_p.close()
        return True
        
        
        

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
        #self._session_progress_table[self._session_id] = self._dict_file_p.tell()
        
        set_buffer(self._session_data_file, self._session_id, self._dict_file_p.tell())

    #----------------------------------------------------------------------
    def force_save(self):
        """Force save"""
        self._save()


    #----------------------------------------------------------------------
    def __del__(self):
        """Close the opened resource"""
        try:
            self.close()
            #self._session_progress_table.close()
        except AttributeError:
            pass

    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.force_save()
        
        if self._dict_file_p.closed:
            pass
        else:
            self._dict_file_p.close()


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

########################################################################
class TESTer(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_bufferop(self):
        """Constructor"""
        ret = get_buffer('filename', 'key')
        set_buffer('filename', 'key', 123)
        self.assertEqual(get_buffer('filename', 'key'), 123)
        
    #----------------------------------------------------------------------
    def test_dp(self):
        """"""
        dp = DictParser(filename='./testdict/subnames_largest.txt', do_continue=True)
        
        for i in range(10):
            print(dp.next())
            


if __name__ == '__main__':
    unittest.main()