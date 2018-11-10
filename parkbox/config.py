import pymysql    #插入pymysql  模块

__author__ = 'kangxiaolong'
__time__ = '2018-01-29'

enable_ssh = False

# 数据库相关配置
db_config = {
    'host': 'sh-cdb-7of3xueq.sql.tencentcdb.com',
    'port': 63529,
    'user': 'develop',
    'passwd': '48bw204I9hKs0R',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'db':'parkbox'
}
