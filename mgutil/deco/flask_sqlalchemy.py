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
    1.0     : 2020/04/28 06:36, MinGo
            1. Created.

'''

# py
from sqlalchemy.exc import IntegrityError

# flask alchemy transaction


__all__ = ["transaction"]


def transaction(session):

    def wrapper(func):
        def sub_wrapper(*args, **kwargs):
            try:
                session.begin(subtransactions=True)
                if ("session" in kwargs):
                    kwargs["session"] = session
                ret = func(*args, **kwargs)
                if (session.is_active):
                    session.commit()
                return ret
            except Exception as e:
                print(e)
                if (session.is_active):
                    session.rollback()
                if (not isinstance(e, IntegrityError)):
                    return {"code": e.code, "data": e.data, "msg": str(e)}
                else:
                    code = -1
                    msg = "DB Error"
                    return {"code": code, "data": 0, "msg": msg}
        return sub_wrapper
    return wrapper
