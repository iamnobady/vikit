#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: core payload
  Created: 05/16/17
"""

import os
import types

#
# DEFINE TYPE
#
TYPE_FILE = 'file'
TYPE_TEXT = 'text'

TYPES = [TYPE_FILE, TYPE_TEXT]

########################################################################
class PayloadEnum(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, payloads, type, name='payload'):
        """Constructor"""
        assert type in TYPES, 'unknow type in payload'
        assert isinstance(payloads, (list, tuple)), 'only support list/tuple as payloads, ' + \
               'got a {}'.format(str(payloads))
        
        self._payloads = list(payloads)
        if type == TYPE_FILE:
            def _check_file(x):
                if not os.path.exists(x):
                    raise AssertionError('not such file: {}'.format(x))

            map(_check_file, self._payloads)
        
        self._iter = iter(self._payloads)
        self._type = type
        
        #
        # set name
        #
        self._name = name
    
    @property
    def name(self):
        """"""
        return self._name
    
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        return self._iter
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        self._iter = iter(self._payloads)
    
    #----------------------------------------------------------------------
    def all(self):
        """"""
        return self._payloads
    
    @property
    def type(self):
        """"""
        return self._type

    #----------------------------------------------------------------------
    def check(self):
        """"""
        #
        # type check when created
        #
        return True
        
        
        

########################################################################
class Payload(PayloadEnum):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, payload, type, name='payload'):
        """Constructor"""
        assert type in TYPES, 'unknow types in payload'
        
        self._payload_s = payload
        PayloadEnum.__init__(self, payloads=list([self._payload_s,]), type=type, name=name)
    
    @property
    def data(self):
        """"""
        return self._payload_s
        
        
        
    
    
    
    