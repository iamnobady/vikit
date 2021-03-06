#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ACK Pool
  Created: 06/02/17
"""

from twisted.internet import task
from ..actions.ackbase import Ack, Ackable
from ..vikitlogger import get_netio_logger

logger = get_netio_logger()

########################################################################
class ACKError(Exception):
    """"""

########################################################################
class _TaskAckable(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, target_func, vargs, kwargs, interval=10, retry_times=5):
        """Constructor"""
        self._id = id
        self._fun  = target_func
        self._vargs = vargs
        self._kwargs = kwargs
        self._interval = interval
        self._retry_times = retry_times

        #
        # priv
        #
        self._count = 0
        self._callback_timeout = None

    #----------------------------------------------------------------------
    def waiting_ack(self):
        """"""
        self._lpc = task.LoopingCall(self._exec)
        self._lpc.start(self._interval, False)

    #----------------------------------------------------------------------
    def _exec(self):
        """"""
        self._count = self._count + 1
        if self._count > self._retry_times:
            self.stop()
            if self._callback_timeout:
                self._callback_timeout(*self._vargs, **self._kwargs)
        else:
            self._fun(*self._vargs, **self._kwargs)

    #----------------------------------------------------------------------
    def stop(self):
        """"""
        if self._lpc.running:
            self._lpc.stop()
        else:
            pass

    #----------------------------------------------------------------------
    def ack(self):
        """"""
        self.stop()

    @property
    def finished(self):
        """"""
        return self._lpc.running
    
    #----------------------------------------------------------------------
    def regist_timeout_callback(self, callback):
        """"""
        assert callable(callback)
        self._callback_timeout = callback





########################################################################
class ACKPool(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._pool = {}
        
        self._callback_timeout_func = None

    #----------------------------------------------------------------------
    def add(self, id, target_func, vargs=tuple(), kwargs={}, ack_timeout=10, retry_items=5):
        """"""
        #
        # build taskackable
        #
        ret = _TaskAckable(id, target_func, vargs, kwargs,
                           interval=ack_timeout, retry_times=retry_items) 
        ret.regist_timeout_callback(self._callback_timeout_func)
        
        self._pool[id] = ret

        ret.waiting_ack()

    #----------------------------------------------------------------------
    def ack(self, id):
        """"""
        _r = self._pool.get(id)
        if _r:
            _r.ack()
            del self._pool[id]
        else:
            logger.warn('[ackpool] no such id:{} in ackpool')
            #raise ACKError('not such id:{} in ackpool'.format(id))
            
        
    #----------------------------------------------------------------------
    def regist_timeout_callback(self, callback):
        """"""
        assert callable(callback)
        self._callback_timeout_func = callback