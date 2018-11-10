# 打开数据库连接
import db
import park_email
from datetime import datetime, timedelta
import time
import redis

res = redis.StrictRedis(host="localhost", port=6379, password="lxx133556")
# 设置,获取单条


'''
数据库指针
'''
conn = db.open_connection()
cursor = conn.cursor()


times = [{"start": 0, "end": 2, "sleep": 60 * 60},
         {"start": 2, "end": 5, "sleep": 60 * 60 * 3},
         {"start": 5, "end": 10, "sleep": 13 * 60},
         {"start": 10, "end": 17, "sleep": 11 * 60},
         {"start": 17, "end": 21, "sleep": 6 * 60},
         {"start": 21, "end": 23, "sleep": 13 * 60},
         {"start": 23, "end": 0, "sleep": 60 * 60}]

t = times

def check_timing_order():
    localtime = datetime.now().strftime(" %H:%M:%S")
    now = datetime.now()
    now = now + timedelta(seconds=-1 * 1)
    start_time = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
    sql = "select count(1) as count from pb_order where status =1 and order_type = 300 and create_time >= '{0}' order by create_time desc ".format(t[0]["start"])
    cursor.execute(sql)
    list1 = cursor.fetchall()
    for row in list1:
        create_time = row.get("count")
        print(create_time)

print(check_timing_order())

print(t[0]["start"])
