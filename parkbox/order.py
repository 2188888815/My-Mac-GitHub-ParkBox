__author__ = 'lixinxu'
__time__ = '2018-07-24'
# 打开数据库连接
import db
import park_email
from datetime import datetime, timedelta
import time
import redis
res = redis.StrictRedis(host="localhost",port=6379,password="lxx133556")

#设置,获取单条


'''
数据库指针
'''
conn = db.open_connection()
cursor = conn.cursor()
number = 0
unit = 3600
'''
时间戳
'''
start_time = int(time.time())/3600 * 3600
'''
n赋值
'''
n = -1
'''
当前小时
'''
now_hour = int(datetime.now().strftime("%H"))

'''
获取数据库订单状况
'''
class OrderCheck:

    #查询数据库订单

    def check_timing_order(self):
        localtime = datetime.now().strftime(" %H:%M:%S")
        now = datetime.now()
        now = now + timedelta(seconds=-10*60)
        start_time = datetime.strftime(now,"%Y-%m-%d %H:%M:%S")
        sql = "select count(1) as count from pb_order where status =1 and order_type = 300 and create_time >= '{0}' order by create_time desc ".format(start_time)
        cursor.execute(sql)
        list1 = cursor.fetchall()
        for row in list1:
            create_time = row.get("count")
            count = create_time
            if count == 0:
                #调用邮件组
                title = "订单异常报警"+start_time
                content = start_time+"------"+localtime+"当前订单数量为："+str(count)
                print(content)
                mail_list = ['kangxiaolong@parkbox.cn', 'zhouxiaoqin@parkbox.cn', '2188888815@qq.com']
                park_email.parkbox_email(content,title,mail_list)
                return content

    #时间戳计算

    def time_stamp(self):
        #调用时间字典
        times = self.do_time()
        for t in times:
            #时间戳
            cur_time = int(time.time())
            hour_stamp = cur_time - (cur_time % unit)
            time_stamp = int(time.time())
            Minute_time = int((time_stamp - hour_stamp) / 60)
            #筛选定制时间条件
            if (now_hour >= t.get("start")) and (now_hour < t.get("end")) and self.check_timing_order():
                if not res.get("check_order_valid_sleep_time"):
                   self.check_timing_order()
                   res.set("check_order_valid_sleep_time", "1", t.get("sleep"))

    #时间字典

    def do_time(self):
        times = [{"start":0,"end":2,"sleep":60*60},
                 {"start":2,"end":5,"sleep":60*60*3},
                 {"start":5,"end":10,"sleep":13*60},
                 {"start":10,"end":17,"sleep":11*60},
                 {"start":17,"end":21,"sleep":6*60},
                 {"start":21,"end":23,"sleep":13*60},
                 {"start":23,"end":0,"sleep":60*60}]
        return times



if __name__ == '__main__':
    while True:
        n += 1
        print("脚本运行第 %s 次" % n)
        time.sleep(4)
        orderchek = OrderCheck()
        orderchek.time_stamp()









