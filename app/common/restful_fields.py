#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   rest_fields.py
@Desc    :   provide user defined flask restful fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/26 23:16, MinGo
          1. Created.

'''

# py

# flask
from flask_restful import fields
from flask_restful.fields import Raw

# local
from . code import RET
from . exception import *

# export
__all__ = [
    "NoEmptyStringField",
    "IntCombinedInStrField",

    "int_record_fields",
]


class NoEmptyStringField(fields.String):

    def format(self, v):
        if (v is None or 0 == len(str(v))):
            raise ValueError()

        return v


class IntCombinedInStrField(fields.String):

    def format(self, v):
        if (v is None or 0 == len(str(v))):
            raise ValueError()

        if (not isinstance(v, str)):
            raise ValueError()

        v_list = []
        for v_s in v.split(","):
            try:
                v_list.append(int(v_s))
            except Exception:
                raise ValueError

        return v_list


def render_data(data, code=RET.S_OK, msg="ok"):
    return {"code": code, "msg": msg, "data": data}


int_record_fields = {
    "msg": fields.String(default="ok"),
    "data": fields.Integer,
}
