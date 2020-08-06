#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_output.py
@Desc    :   provide session output fields definitions
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
from .session_output_value import session_output_value_record_field

# export
__all__ = [
    'session_output_record_field',
    'session_output_record_fields',
    'session_output_records_fields'
]


# local fields
#
session_output_record_field = {
    'id': fields.Integer,
    'session_id': fields.String,
    'module_name': fields.String,
    'key': fields.String,
    'index': fields.Integer,
    'data_type': fields.Integer,
    'value': fields.String,
}


# API fields
#
session_output_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(session_output_record_field),
}

session_output_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(session_output_record_field)),
}
