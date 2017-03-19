#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Mixer for multiparser!
  Created: 03/09/17
"""

import unittest

from .dict_parser import DictParser
from ..utils.iter_utils import iter_mix


#DictParser(filename)

DEFAULT_SESSION_ID = 'default_session_id_{index}'
DEFAULT_SESSION_FILENAME = 'session.dat'

########################################################################
class DictParserMixer(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, file_list, do_continue=True, session_id=DEFAULT_SESSION_ID,
                 session_filename=DEFAULT_SESSION_FILENAME):
        """Constructor"""
        self._dict_parsers = []
        for i in range(len(file_list)):
            self._dict_parsers.append(DictParser(file_list[i],session_id=DEFAULT_SESSION_ID.format(index=i), 
                                                 do_continue=do_continue,
                                                 session_data_file=session_filename))

        self._mixer = iter_mix(*tuple(self._dict_parsers))

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
        for i in self._mixer:
            return i
        else:
            raise StopIteration()

    #----------------------------------------------------------------------
    def save(self):
        """"""
        map(lambda x: x.force_save(), self._dict_parsers)

    #----------------------------------------------------------------------
    def force_save(self):
        """"""
        self.save()

    #----------------------------------------------------------------------
    def get_current_poses(self):
        """"""
        self._current_poses = map(lambda x: x.get_current_pos(), self._dict_parsers)
        return self._current_poses

    #----------------------------------------------------------------------
    def get_current_pos(self):
        """"""
        return sum(self.get_current_poses())

    #----------------------------------------------------------------------
    def get_total_sizes(self):
        """"""
        self._total_sizes = map(lambda x: x.get_total_size(), self._dict_parsers)
        return self._total_sizes

    #----------------------------------------------------------------------
    def get_total_size(self):
        """"""
        return reduce(lambda x,y: x * y, map(int, self.get_total_sizes()))

    #----------------------------------------------------------------------
    def close(self):
        """"""
        map(lambda x: x.close(), self._dict_parsers)

    #----------------------------------------------------------------------
    def reset(self):
        """"""
        map(lambda x: x.reset(), self._dict_parsers)





if __name__ == '__main__':
    unittest.main()