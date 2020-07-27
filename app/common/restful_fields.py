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
import json
from datetime import date
from datetime import datetime

# flask
from flask_restful import fields
from flask_restful.fields import get_value
from flask_restful.fields import String
from flask_restful.fields import MarshallingException


# local
from . code import RET
from .db import base_db_processor
from . exception import *

# export
__all__ = [
    "NoEmptyStringField",
    "IntCombinedInStrField",
    "DateTimeStrField",
    "int_record_fields",
]


class NoEmptyStringField(String):

    def format(self, v):
        if (v is None or 0 == len(str(v))):
            error_msg = ("Input string empty.")
            raise MarshallingException(error_msg)

        return v


class IntCombinedInStrField(String):

    def format(self, value):
        v = String.format(self, value)

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
        return self.format(get_value(self.attribute, self.default))

    def translate(self, escape_tab):
        return super().format(get_value(self.attribute, self.default))


class DateTimeStrField(String):

    def format(self, value):
        v = String.format(self, value)

        try:
            dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            dt = dt
        except Exception:
            try:
                dt = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                dt = dt
            except Exception:
                error_msg = (
                    "Datetime[%s] format ERROR type." % (v))
                raise MarshallingException(error_msg)
            v = v.replace("T",   " ")

        return v

    def output(self, key, obj):
        return self.format(get_value(self.attribute, self.default))

    def translate(self, escape_tab):
        return super().format(get_value(self.attribute, self.default))


class DictStrField(String):

    def format(self, value):
        v = String.format(self, value)

        if (isinstance(v, dict)):
            return v

        try:
            json.loads(v)
        except Exception:
            msg = ("DictStr[%s] format ERROR" % (v))
            raise MarshallingException(msg)

        return v

    def output(self, key, obj):
        return self.format(get_value(self.attribute, self.default))

    def translate(self, escape_tab):
        return super().format(get_value(self.attribute, self.default))


class result_json_encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, base_db_processor):
            json_obj = obj.to_json()
            return json_obj
        else:
            return json.JSONEncoder.default(self, obj)


def render_data(data, code=RET.S_OK, msg="ok"):
    if (not isinstance(data, (dict, list, base_db_processor))):
        json_obj = {"code": code, "msg": msg, "data": data}
        return json_obj
    elif (isinstance(data, list)):
        if (data and isinstance(data[0], base_db_processor)):
            data_list = []
            for d in data:
                data_list.append(d.to_json())
            json_obj = {"code": code, "msg": msg, "data": data_list}
        else:
            json_obj = json_obj = {"code": code, "msg": msg, "data": data}
        return json_obj
    elif (isinstance(data, base_db_processor)):
        json_obj = {"code": code, "msg": msg, "data": data.to_json()}
        return json_obj
    elif (3 == len(set(["code", "data", "msg"]) & set(data.keys()))):
        return data

    json_obj = {"code": code, "msg": msg, "data": data}
    return json_obj


int_record_fields = {
    "code": fields.Integer,
    "msg": fields.String(default="ok"),
    "data": fields.Integer,
}

str_record_fields = {
    "code": fields.Integer,
    "msg": fields.String(default="ok"),
    "data": fields.String,
}


raw_record_fields = {
    "code": fields.Integer,
    "msg": fields.String(default="ok"),
    "data": fields.Raw,
}
