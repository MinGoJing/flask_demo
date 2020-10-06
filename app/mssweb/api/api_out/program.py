#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   program.py
@Desc    :   provide program result fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/28 23:25, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# export
__all__ = [
    'program_record_field',
    'program_record_fields',
    'program_records_fields'
]


# local fields
#
program_record_field = {
    'id': fields.Integer,
    "utility_id": fields.Integer,
    "utility_name": fields.String,
    "version": fields.String,
    "provider_employee_id": fields.Integer,
    "provider_employee_name": fields.String,
    "description": fields.String,
    'disabled': fields.Boolean,
    'operator_id': fields.Integer,
    'operator_name': fields.String,
    'operate_time': fields.DateTime(dt_format='iso8601'),
}


# API fields
#
program_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(program_record_field),
}

program_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(program_record_field)),
}
