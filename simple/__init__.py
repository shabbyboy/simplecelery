# -*- coding: utf-8 -*-

'''
simplecelery @2019 03 26
author xuxiaolong

redis 作为broker
redis 作为结果返回result_backend
'''
from time import sleep
from utils.base import BaseTask
import json
import multiprocessing

from importlib import import_module
from utils.redisbase import RedisHelper
class Celery(object):
    def __init__(self, name):
        self.name = name
        self.taskdic = dict()
        self._task = dict()
        self.queuedic = dict()

    def start(self):
        '''
        启动方法
        从redis list 中获取message ，并找到对应的任务实例去执行，通过调用task.runtask()方法执行
        '''
        queue = set([v["queue"] for v in self.taskdic.values()])
        def runloop(queue):
            _redis = RedisHelper.getredisconn()

            while True:
                retjson = _redis.Lpop(queue)
                if retjson is None:
                    sleep(5)
                    continue
                message = json.loads(retjson)
                for fun in self.queuedic[queue]:
                    if message["name"] == fun.split(".")[-1:][0]:
                        self._task[message["name"]](*message["args"],**message["kwargs"])


        for q in queue:
            runloop(q)




    def config_from_object(self, include=None):
        '''获取基本的配置信息'''
        self.config = import_module(include)
        # redis_url 配置redis地址信息
        redis,hostpass, portdb = self.config.redis_url.split(':')
        password, host = hostpass.split('@')
        port, db = portdb.split('/')
        # celery_route配置路由信息
        self.taskdic = self.config.celery_route

        #获取数据库连接配置后，初始化数据库连接，之后通过getrediscon获取数据库连接实例
        redis = RedisHelper(host, port, db, password)

        for k,v in self.taskdic.items():
            if v["queue"] not in self.queuedic.keys():
                self.queuedic[v["queue"]] = [k]
            else:
                self.queuedic[v["queue"]].append(k)


    #任务装饰器
    def task(self,*args,**kwargs):
        #print args,kwargs
        def create_inner_task():
            def create_tasks(func):
                ret = self.create_task_fromfun(func)
                return ret
            return create_tasks
        return create_inner_task()

    #通过函数创建任务对象
    def create_task_fromfun(self,func):
        tasks = type(func.__name__, (BaseTask,), dict({'name':func.__name__,'run': staticmethod(func)}))()
        #print isinstance(tasks,BaseTask)
        if tasks.name not in self._task:
            self._task[tasks.name] = tasks.run
        tasks.bind(self)
        return tasks