# simplecelery
## 简单模拟了celery 在一台机器上让另一台机器执行任务的功能，不过没有重试
### 文件介绍
celery 包是celery类所在的位置  
util 是 数据库连接 和 任务类


### example 是我自己写的一个例子：
python -m example.celery  启动celery，部署在服务端

python -m example.run 是客户端需要执行的，告诉客户端开始执行任务
具体任务，参照add的写法，

config文件是相关配置，redis_url 配置broker  celery_route 是绑定任务和队列


