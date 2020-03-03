# coding: utf-8
import pymysql
import db

ORDER_ID = 'test upload21'
USER_ID = 999
COMMISSION_RATE = 0.75

conn = pymysql.connect(**db.config)
cursor = conn.cursor()


# 订单号匹配
def order_num_pattern():
    sql = "SELECT * FROM tb_order WHERE tb_p_oid = '%s'" % ORDER_ID
    cursor.execute(sql)
    orders = cursor.fetchall()
    # 订单号是否存在于数据库中
    if orders == '':
        return {'code': 401, 'msg': '订单号不存在'}
    # 看下是不是自己绑定过的，不是自己的就是被别人绑定过
    sql = "SELECT * FROM tb_order WHERE tb_p_oid = '%s' AND user_id <> 0 GROUP BY user_id" % ORDER_ID
    bind = cursor.execute(sql)
    # bind: 0没有被绑定过; 1被一人绑定过，查下是不是本人; >1之前绑定异常了，多条数据只会有同一个user_id
    if bind == 1:
        if cursor.fetchone()[1] == USER_ID:
            return {'code': 402, 'msg': '亲，您已经绑定过订单了哦～'}
        else:
            return {'code': 403, 'msg': '订单已被用户ID:' + cursor.fetchone()[1] + '绑定过'}
    elif bind > 1:
        # todo: 异常处理，记录日志
        print()
    # 是否发送过淘口令，防止刷数据
        # todo: 查询淘口令表是否有查询过此商品
    pay_money = 0
    rebate = 0
    for i in orders:
        # 看下该订单号是否状态为已付款
        if i[10] != 10:
            conn.rollback()
            return {'code': 404, 'msg': '订单状态无效'}
        sql = "UPDATE tb_order SET user_id = '%s' WHERE id = '%s'" % (USER_ID, i[0])
        cursor.execute(sql)
        conn.commit()
        # 返回实付金额、返利金额
        pay_money += float(i[11])
        rebate += float(i[17])
    cursor.close()
    return {'code': 101, 'pay_money': '%.2f' % pay_money, 'rebate': '%.2f' % (rebate * COMMISSION_RATE)}


# 查找库中用户
def find_user():
    remark_name = 'lee'


# 正则单号
def regular_order_num():
    # todo 正则单号
    print()


ret = order_num_pattern()
print(ret)
