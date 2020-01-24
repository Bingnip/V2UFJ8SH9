# coding: utf-8
import pymysql
import db

USER_ID = 999

conn = pymysql.connect(**db.config)
cursor = conn.cursor()


# 查看钱包
def wallet_master():
    # status: 10(未收货金额) 20(可提现金额)
    sql = "SELECT sum(tb_pay_income) FROM tb_order WHERE user_id = '%s' AND tb_status = 10" % USER_ID
    cursor.execute(sql)
    not_receive = cursor.fetchone()[0]
    if not_receive is None:
        not_receive = 0
    sql = "SELECT sum(tb_clear_income) FROM tb_order WHERE user_id = '%s' AND tb_status = 20" % USER_ID
    cursor.execute(sql)
    can_withdraw = cursor.fetchone()[0]
    if can_withdraw is None:
        can_withdraw = 0


# 找出用户id
def find_user():
    print()


ret = wallet_master()
print(ret)
