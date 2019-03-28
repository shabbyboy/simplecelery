# -*- coding: utf-8 -*-

'''
simplecelery @2019 03 26
author xuxiaolong

redis 作为broker
redis 作为结果返回result_backend
'''

from utils.base import BaseTask

from importlib import import_module
from utils.redisbase import RedisHelper
class Celery(object):
    def __init__(self, name):
        self.name = name

    def start(self):
        '''
        启动方法
        从redis list 中获取message ，并找到对应的任务实例去执行，通过调用task.runtask()方法执行
        '''
        _redis = RedisHelper(self.host,self.port,self.db,self.password)
        while True:
            pass



    def config_from_object(self, include=None):
        '''获取基本的配置信息'''
        self.config = import_module(include)
        # redis_url 配置redis地址信息
        redis, _, hostpass, portdb = self.config.redis_url.split(':')
        self.password, self.host = hostpass.split('@')
        self.port, self.db = portdb.split('/')
        # celery_route配置路由信息
        self.taskdic = self.config.celery_route

    #任务装饰器
    def task(self,*args,**kwargs):
        def create_inner_task(*args,**kwargs):
            def create_tasks(func):
                ret = self.create_task_fromfun(func)
                return ret
            return create_tasks
        return create_inner_task(*args,**kwargs)

    #通过函数创建任务对象
    def create_task_fromfun(self,func):
        tasks = type(func.__name__, (BaseTask,), dict({'name':func.__name__,'run': staticmethod(func)}))()
        if tasks.name not in self._task:
            self._task[tasks.name] = tasks
        tasks.bind(self)
        return tasks