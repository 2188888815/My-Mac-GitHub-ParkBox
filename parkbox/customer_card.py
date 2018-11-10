import random
import time
import config
import db
__author__ = 'kangxiaolong'
__time__ = '2018-02-23'



'''
    将原来年卡会员同步到新表
'''
conn = db.open_connection()
cursor = conn.cursor()

'''
    同步年卡信息
'''
def sync_coupons():

    sql = " select `ccid`, `customer_id`, `type`, `card_type`, `venue_id`, `total_price`, `real_pay`, `ctime`," \
          " `start_time`, `end_time`, `terminal`, `is_active`, `is_del`, `modify_time` " \
          " from pb_customer_cards "
    cursor.execute(sql)
    list = cursor.fetchall()
    if list:
        for row in list:
            print  (row.get("ccid"))

            ctime = time.localtime(row.get("ctime"))
            ctime = time.strftime("%Y-%m-%d %H:%M:%S", ctime)
            sql = " select `id`,`modify_time` from pb_operation_customer_coupon where customer_id = {0} and create_time ='{1}' "\
                .format(row.get("customer_id"),ctime)
            cursor.execute(sql)
            check_coupon = cursor.fetchone()

            if check_coupon:
                if row.get("modify_time") != check_coupon.get("modify_time"):
                    update_coupons(row,check_coupon.get("id"))
            else:
                save_coupons(row)


'''
    保存用户卡券信息
'''
def save_coupons(row):
    # 取出卡券信息
    coupon_type_code = "NK-" + str(row.get("card_type")).zfill(3) + "-001"
    sql = " select `id`, `coupon_name`, `subtitle`, `description`, `coupon_title`, `coupon_type_code`, " \
          "  `city_id`, `start_time`, `end_time`, `discount_type`, `discount_way`, `denomination`, `price`," \
          " `vip_price`, `renew_price`, `expire_days`, `scope`, `limit_type`, `limit_amount`, `limit_gain`, `limit_number`," \
          " `issue_amount`, `is_show` " \
          " from pb_operation_coupons where coupon_type_code = '{0}'".format(coupon_type_code)
    cursor.execute(sql)
    coupons = cursor.fetchone()
    if not coupons:
        return

    sql = " select a.`id`, a.`category`, a.`operation_type_name`, a.`operation_type_code`, a.`title`, a.`subtitle`, a.`description` " \
          " from `pb_operation_type` a left join `pb_operation_activity_coupon` " \
          " b on a.`operation_type_code` = b.activity_code where b.coupon_type_code = '{0}' ".format(
        coupons.get("coupon_type_code"))
    cursor.execute(sql)
    operation_type = cursor.fetchone()

    operation_type_code = ""
    operation_type_name = ""
    if operation_type:
        operation_type_code = operation_type.get("operation_type_code"),
        operation_type_name = operation_type.get("operation_type_name")

    # 创建时间
    ctime = time.localtime(row.get("ctime"))
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", ctime)

    # 更新时间
    if row.get("mtime"):
        mtime = time.localtime(row.get("mtime"))
        mtime = time.strftime("%Y-%m-%d %H:%M:%S", mtime)
    else:
        mtime = ctime

    # 开始时间
    start_time = time.localtime(row.get("start_time"))
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)

    # 结束时间
    end_time = time.localtime(row.get("end_time"))
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
    coupon_code = gen_coupon_code()

    sql = " INSERT INTO `pb_operation_customer_coupon` (" \
          " category,`operation_type_code`, `operation_type_name`, `coupon_type_id`, `coupon_type_code`," \
          " `coupon_name`, `coupon_code`, `customer_id`," \
          " `city_id`, `discount_type`, `discount_way`," \
          " `denomination`, `price`,`real_pay`,  `expire_days`, `start_time`," \
          " `end_time`, `channel_name`,  `limit_type`, `limit_amount`," \
          " `limit_number`,`limit_products`, `scope`, " \
          "  `is_show`, `is_valid`, `creator`," \
          " `create_time`, `modify_time`, `is_deleted`)" \
          " VALUES(" \
          "%s,%s,%s,%s,%s," \
          "%s,%s,%s," \
          "%s,%s,%s," \
          "%s,%s,%s,%s,%s," \
          "%s,%s,%s,%s," \
          "%s,%s,%s," \
          "%s,%s,%s," \
          "%s,%s,%s" \
          ")"

    cursor.execute(sql,
                   (
                       1,
                       operation_type_code,
                       operation_type_name,
                       coupons.get("id"),
                       coupons.get("coupon_type_code"),
                       coupons.get("coupon_name"),
                       coupon_code,
                       row.get("customer_id"),
                       coupons.get("city_id"),
                       coupons.get("discount_type"),
                       coupons.get("discount_way"),
                       coupons.get("denomination"),
                       coupons.get("price"),
                       row.get("real_pay"),
                       coupons.get("expire_days"),
                       start_time,
                       end_time,
                       '老数据同步',
                       coupons.get("limit_type"),
                       coupons.get("limit_amount"),
                       coupons.get("limit_number"),
                       row.get("venue_id"),
                       coupons.get("scope"),
                       coupons.get("is_show"),
                       row.get("is_active"),
                       '自动同步',
                       ctime,
                       mtime,
                       row.get("is_del")
                   )
                   )
    conn.commit()


'''
    生成用户卡券编码
'''


def gen_coupon_code():
    code = "".join(random.sample('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', 12))
    sql = " select `coupon_code` " \
          " from pb_operation_customer_coupon where coupon_code = '{0}'".format(code)
    cursor.execute(sql)
    rs = cursor.fetchone()
    if rs:
        gen_coupon_code()

    return code


'''
    更新用户卡券状态
'''


def update_coupons(row , id):
    sql = "  UPDATE `pb_operation_customer_coupon` SET" \
          "  `is_valid` = %s, " \
          " `modify_time` = %s, `is_deleted` = %s, `limit_products` = %s" \
          " where id = %s "

    cursor.execute(sql,
                   (
                       row.get("is_active"),
                       row.get("modify_time"),
                       row.get("is_del"),
                       row.get("venue_id"),
                       id
                   )
                   )
    conn.commit()

if __name__ == '__main__':
    sync_coupons()
    print ('OK')
