__author__ = 'DELL'
# -*- coding: utf-8 -*-
import sys
import MySQLdb
from pipes import SOURCE
from compiler.transformer import Transformer
from _sqlite3 import Cursor, SQLITE_ALTER_TABLE
from com.python_test.test_mysqldb import sql, cursor
class TransformerMoney(object):

    def __init__(self,conn):
        self.conn = conn
    def check_acct_available(self,acctid):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acctid='%s'" %acctid
#             print sql
            cursor.execute(sql)
            print ("check_acct_available: %s " % sql)
            rs = cursor.fetchall()
            if  len(rs) !=1:
                raise Exception("账号s%校验失败" % acctid)
        finally:
            cursor.close()

    def has_enough_money(self,acctid,money):
        cursor = self.conn.cursor()
        try:

            sql = "select * from account where  acctid=%s and money>%s" % (acctid, money)
            print (sql)
            cursor.execute(sql)
            print ("has_enough_money: " + sql)
            rs = cursor.fetchall()
            print len(rs)
            if  len(rs) !=1:
                raise Exception("账户s%金额不够��" % acctid)
        finally:
            cursor.close()

    def reduce_money(self,acctid,money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money= money-%s where acctid='%s'"% (money,acctid)
            cursor.execute(sql)
            print (sql)
            if  cursor.rowcount != 1:
                raise Exception("账户s%扣款失败" % acctid)
        finally:
            cursor.close()

    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money+%s where acctid='%s'"% (money,acctid)
            cursor.execute(sql)
            rs = cursor.fetchall()
            if  cursor.rowcount != 1:
                raise Exception("%s转账失败！" % acctid)
        finally:
            cursor.close()


    def transfer(self,source_acctid,target_acctid,money):
        try:
            self.check_acct_available(source_acctid)
            self.check_acct_available(target_acctid)
            self.has_enough_money(source_acctid,money)
            self.reduce_money(source_acctid,money)
            self.add_money(target_acctid,money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


if  __name__ == "__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]

    conn = MySQLdb.connect(host='192.168.234.139',user='mm100',passwd='mm100',db='mama100',port=3306,charset="utf8")
    tr_money = TransformerMoney(conn)

    try:
        tr_money.transfer(source_acctid,target_acctid,money)

    except Exception as e:
        print ("出现问题" + str(e))
    finally:
        conn.close()
