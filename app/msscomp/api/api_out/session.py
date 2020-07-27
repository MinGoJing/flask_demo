#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session api output
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/23 06:45, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# local
from .session_input import session_input_record_field
from .session_output import session_output_record_field
from .session_parameter import session_parameter_record_field

# export
__all__ = [
    'session_record_field',
    'session_record_fields',
    'session_records_fields'
]


# local fields
#
session_record_field = {
    'id': fields.Integer,
    'instance_id': fields.Integer,
    'init_time': fields.DateTime(dt_format='iso8601'),
    'start_time': fields.DateTime(dt_format='iso8601'),
    'end_time': fields.DateTime(dt_format='iso8601'),
    'status': fields.Integer,
    'note': fields.String,
    'session_inputs': fields.List(fields.Nested(session_input_record_field)),
    'session_outputs': fields.List(fields.Nested(session_output_record_field)),
    'session_parameters': fields.List(fields.Nested(session_parameter_record_field))
}


# API fields
#
session_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(session_record_field),
}

session_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(session_record_field)),
}
