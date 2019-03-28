# -*- coding: utf-8 -*-


class BaseTask(object):
    '''
    任务类的基类，所有任务的拓展都继承此类
    '''


    def runtask(self,*args,**kwargs):
        '''
        任务执行的方法
        '''

    @classmethod
    def bind(cls,app):
        '''
        绑定app实例到task
        '''
        cls._app = app









