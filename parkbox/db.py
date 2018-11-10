__author__ = 'kangxiaolong'
__time__ = '2018-01-29'

import config
import pymysql

'''
    创建数据库连接
'''
def open_connection():
    conn = pymysql.connect(**config.db_config)
    return conn


if __name__ == '__main__':
    conn = open_connection()
    cursor = conn.cursor()
    count = cursor.execute(
        "select * from pb_order limit 2 ")
    # list = cursor.fetchall()
    print (count)
    print ('OK!')

