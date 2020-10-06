#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   flask_sqlalchemy.py
@Desc    :   provide sqlalchemy associated decorators
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :
    1.0     : 2020/04/28 06:36, MinGo
            1. Created.

'''

# py
import inspect
from werkzeug.exceptions import HTTPException

# flask
from flask import abort
from flask import request
from flask import make_response
from sqlalchemy.exc import DBAPIError


__all__ = ["transaction"]


def transaction(session):

    def trans_wrapper(func):
        def sub_trans_wrapper(*args, **kwargs):
            try:
                session.begin(subtransactions=True)
                # use same session throughout the transaction
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

                b_request_bounded = None
                try:
                    str(request)
                    b_request_bounded = True
                except Exception as ee:
                    ee = ee
                    b_request_bounded = False

                if (b_request_bounded):
                    if (isinstance(e, HTTPException)):
                        resp = e.get_response()
                        abort(resp)
                    elif (isinstance(e, DBAPIError)):
                        if (hasattr(e, "orig") and 2 <= len(e.orig.args)):
                            e_args = e.orig.args
                            code = -(e_args[0])
                            msg = e_args[1]
                            return {"code": code, "data": 0, "msg": msg}
                        else:
                            code = e.code
                            msg = str(e)
                        resp = make_response({"code": code, "data": 0, "msg": msg}, 500,
                                             {"Content-Type": "application/json"})
                        abort(resp)
                    else:
                        resp = make_response({"code": -1, "data": 0, "msg": str(e)}, 500,
                                             {"Content-Type": "application/json"})
                        abort(resp)
                else:  # not request bounded
                    if (isinstance(e, HTTPException)):
                        if (hasattr(e, "result_code")):
                            return {"code": e.result_code, "data": 0, "msg": e.msg}
                    elif (isinstance(e, DBAPIError)):
                        if (hasattr(e, "orig") and 2 <= len(e.orig.args)):
                            e_args = e.orig.args
                            code = -(e_args[0])
                            msg = e_args[1]
                        else:
                            code = e.code
                            msg = str(e)

                        return {"code": e.code, "data": 0, "msg": msg}
                    else:
                        return {"code": e.code, "data": 0, "msg": e.description}

                raise (e)

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
