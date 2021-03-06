#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define HeartBeat
  Created: 06/18/17
"""

import psutil

from . import base

from ..vikitdatas import healthinfo

########################################################################
class HeartBeatAction(base.BaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_node_id, service_infos, health_info=None):
        """Constructor"""
        self.service_node_id = service_node_id
        
        assert isinstance(service_infos, list)
        self.service_infos = service_infos

        if health_info:
            assert isinstance(health_info, healthinfo.HealthInfo)
        else:
            health_info = healthinfo.HealthInfo(cpu_percent=psutil.cpu_percent(),
                                                ram_percent=psutil.virtual_memory().percent)
        self.health_info = health_info
        
    @property
    def id(self):
        """"""
        return self.service_node_id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<HeartBeat from service_node_id:{}>'.format(self.id)
        
        
    
    