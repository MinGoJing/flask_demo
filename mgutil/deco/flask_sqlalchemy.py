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
import inspect
from werkzeug.exceptions import HTTPException

# flask
from flask import abort, make_response


__all__ = ["transaction"]


def transaction(session):

    def trans_wrapper(func):
        def sub_trans_wrapper(*args, **kwargs):
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

                if (isinstance(e, HTTPException) and hasattr(e, "status")):
                    resp = make_response(
                        e.get_response(), e.status, e.get_headers())
                    abort(resp)

                raise (e)

                # if (not isinstance(e, (IntegrityError, TypeError, AttributeError))):
                #     return {"code": e.code, "data": e.data, "msg": str(e)}
                # elif isinstance(e, IntegrityError):
                #     if (hasattr(e, "orig") and 2 <= len(e.orig.args)):
                #         e_args = e.orig.args
                #         code = -(e_args[0])
                #         msg = e_args[1]
                #         return {"code": code, "data": 0, "msg": msg}
                #     else:
                #         code = e.code
                # elif isinstance(e, AttributeError):
                #     code = -2
                # elif isinstance(e, TypeError):
                #     code = -3
                # else:
                #     code = -9
                # return {"code": code, "data": 0, "msg": str(e)}

        return sub_trans_wrapper
    return trans_wrapper


def api_tansaction_deep():
    transaction_deep = 0
    stacks = inspect.stack()
    for st in stacks:
        filename = st.filename
        func = st.function

        if (filename.count("flask_sqlalchemy")
                and func.count("sub_trans_wrapper")):
            transaction_deep += 1
            continue

        if (filename.count("flask")
            and filename.count("views")
                and func.count("view")):
            break

    return transaction_deep
