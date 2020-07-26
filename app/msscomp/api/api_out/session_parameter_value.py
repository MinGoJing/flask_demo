#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_parameter_value.py
@Desc    :   provide session parameter value fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/24 06:00, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# export
__all__ = [
    'session_parameter_value_record_field',
    'session_parameter_value_record_fields',
    'session_parameter_value_records_fields'
]


# local fields
#
session_parameter_value_record_field = {
    'id': fields.Integer,
    "session_parameter_id": fields.Integer,
    "key": fields.String,
    "index": fields.Integer,
    "data_type": fields.String,
    "v1": fields.String,
    "v2": fields.String,
    "v3": fields.String
}


# API fields
#
session_parameter_value_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(session_parameter_value_record_field),
}

session_parameter_value_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(session_parameter_value_record_field)),
}
