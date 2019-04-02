# -*- coding: utf-8 -*-

import redis

class RedisHelper(object):

    #节省点内存空间，积少成多
    __slots__ = ('con','connect',)

    def __new__(cls, *args, **kwargs):
        if isinstance(cls.con,RedisHelper):
            return cls.con
        cls.con = object.__new__(cls)
        return cls.con

    def __init__(self,host,port,db,password):
        #对象连接池，避免每次都新实例出连接池,所以用一个类实例成员
        conpool = redis.ConnectionPool(host=host,port=port,db=db,password=password)
        self.connect = redis.Redis(connection_pool=conpool)

    #通过一个类方法获取连接，不用每次都实例话，将是实例话放在app，初始化的地方
    @classmethod
    def getredisconn(cls):
        if cls.con:
            return cls.con
        return None

    def publish(self,chanel,msg):
        '''
        发布
        :return:
        '''
        return self.connect.publish(chanel,msg)

    def subscribe(self,chanel):
        '''
        订阅
        :return:
        '''
        pub = self.connect.pubsub()
        pub.subscribe(chanel)
        pub.parse_response()
        return pub

    def Lpush(self,key,value):
        return self.connect.lpush(key,value)

    def Lpop(self,key):
        return self.connect.lpop(key)

    def Rpush(self,key,value):
        return self.connect.rpush(key,value)

    def Rpop(self,key):
        return self.connect.rpop(key)

