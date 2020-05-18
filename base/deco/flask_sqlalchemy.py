#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   flask_sqlalchemy.py
@Desc    :   provide sqlalchemy associated decorators
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/04/28 06:36, MinGo
          1. Created.

'''

# py

# flask alchemy transaction


def alchemy_transaction(session):
    def wrapper(func):
        def sub_wrapper(*args, **kwargs):
            try:
                session.begin(subtransactions=True)
                func(*args, **kwargs)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return sub_wrapper
    return wrapper
