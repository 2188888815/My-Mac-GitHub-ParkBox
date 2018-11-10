import time

import redis
res = redis.StrictRedis(host="localhost",port=6379,password="lxx133556")
#设置,获取单条

res.set("p1","good1",12)

print(res.get("p1"))
time.sleep(13)
print(res.get("p1"))

#缓冲多条命令,减少服务器-客户端之间的tcp数据包

pipe = res.pipeline()

pipe.set("p2","nice")

pipe.set("p3","handson")

pipe.set("p4","cool")

pipe.execute()
