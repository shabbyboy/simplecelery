# -*- coding: utf-8 -*-
import json
from .redisbase import RedisHelper
class BaseTask(object):
    '''
    任务类的基类，所有任务的拓展都继承此类
    '''
    def runtask(self,*args,**kwargs):
        '''
        任务执行的方法
        '''

        #数据库连接坐下修改
        _redis = RedisHelper.getredisconn()

        messagedic = dict()
        messagedic["name"] = self.name
        messagedic["args"] = args
        messagedic["kwargs"] = kwargs
        #self.run(*args,**kwargs)

        for k,v in self._app.taskdic.items():
            if k.split(".")[-1:][0] == self.name:
               _redis.Lpush(v["queue"],json.dumps(messagedic))


    def bind(self,app):
        '''
        绑定app实例到task
        '''
        self._app = app









