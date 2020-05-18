#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mysql.py
@Desc    :   provide Mysql connection services.
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/04/28 21:25, MinGo
          1. Created.

'''

# py

# db
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

# export
__all__ = ["Mysql"]


class Mysql(object):
    """
        同时提供MySql数据库连接池、数据库客户端的功能

    Usage:
        1. Init: 
    """
    # 连接池对象
    __pool = None

    def __init__(self, mincached=10, maxcached=20, maxshared=10, maxconnections=200, blocking=True,
                 maxusage=100, setsession=None, reset=True,
                 host='127.0.0.1', port=3306, db='test',
                 user='root', password='123456', charset='utf8'):
        """
        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
        """
        if (not Mysql.__pool):
            Mysql.__pool = PooledDB(
                creator=pymysql,
                mincached=mincached, maxcached=maxcached, maxshared=maxshared,
                maxconnections=maxconnections, blocking=blocking,
                maxusage=maxusage, setsession=setsession, reset=reset,
                host=host, port=port, db=db,
                user=user, password=password, charset=charset,
                cursorclass=DictCursor
            )
            self.__pool = Mysql.__pool
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    @staticmethod
    def get_conn(**config):
        if (not Mysql.__pool):
            if (config):
                return Mysql(config)
            else:
                raise Exception("Mysql Client NOT Initialized.")
        return Mysql()

    def get_one(self, sql, param=()):
        """
        查询单个结果
        """
        if (param is None):
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = None
        return result

    def get_all(self, sql, param=()):
        """
        查询多个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)

        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = []
        return count, result

    def get_many(self, sql, num, param=()):
        if (param is None):
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)

        if (count):
            result = self._cursor.fetchmany(num)
        else:
            result = []
        return count, result

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        return count

    def execute(self, sql, param=()):
        count = self.__execute(sql, param)
        return count

    def __get_insert_id(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def insert_one(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__get_insert_id()

    def insert_many(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: SQL格式及条件，使用(%s,%s)
        @param param: 要更新的值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if ('commit' == option):
            self._conn.commit()
        else:
            self._conn.rollback()

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print(e)

    def dispose(self, b_end=True):
        """
        @summary: 释放连接池资源
        """
        if (b_end):
            self.end('commit')
        else:
            self.end('rollback')
        self.close()
