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
from flask_restful.fields import MarshallingException


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
            error_msg = ("Input string empty.")
            raise MarshallingException(error_msg)

        return v


class IntCombinedInStrField(fields.String):

    def format(self, value):
        v = super().format(value)

        if (v is None or 0 == len(str(v))):
            error_msg = ("Int list in len(0).")
            raise MarshallingException(error_msg)

        if (not isinstance(v, str)):
            error_msg = ("Int list NOT in string type.")
            raise MarshallingException(error_msg)

        v_list = []
        for v_s in v.split(","):
            try:
                v_list.append(int(v_s))
            except Exception:
                error_msg = (
                    "Int list items(seperated with ',') NOT in int type.")
                raise MarshallingException(error_msg)

        return v_list

    def output(self, key, obj):
        return self.format(self.attribute)

    def translate(self, escape_tab):
        return super().format(self.attribute)


def render_data(data, code=RET.S_OK, msg="ok"):
    return {"code": code, "msg": msg, "data": data}


int_record_fields = {
    "msg": fields.String(default="ok"),
    "data": fields.Integer,
}
