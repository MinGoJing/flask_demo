#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_parameter.py
@Desc    :   provide session parameter definitions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/24 05:40, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# local
from .session_parameter_value import session_parameter_value_record_field

# export
__all__ = [
    'session_parameter_record_field',
    'session_parameter_record_fields',
    'session_parameter_records_fields'
]


# local fields
#
session_parameter_record_field = {
    'id': fields.Integer,
    'name': fields.String,
    'index': fields.Integer,
    'note': fields.String,
    'session_id': fields.Integer,
    "parameter_values": fields.List(fields.Nested(session_parameter_value_record_field))
}


# API fields
#
session_parameter_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(session_parameter_record_field),
}

session_parameter_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(session_parameter_record_field)),
}
