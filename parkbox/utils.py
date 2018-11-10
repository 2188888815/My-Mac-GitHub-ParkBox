import db

__author__ = 'kangxiaolong'
__time__ = '2018-03-01'

conn = db.open_connection()
cursor = conn.cursor()

'''
    判断数据库中表是否存在
'''
def exist_of_table(table_name):
    sql = "show TABLES like '{0}'".format(table_name)
    cursor.execute(sql)
    list = cursor.fetchall()
    if list:
        return True;
    return False

if __name__ == '__main__':
    print (exist_of_table("pb_order1"))
    print ('OK')
