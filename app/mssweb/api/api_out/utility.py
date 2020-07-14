#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utility.py
@Desc    :   provide utility fields definition
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/13 05:26, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# export
__all__ = [
    'utility_record_field',
    'utility_record_fields',
    'utility_records_fields'
]


# local fields
#
utility_record_field = {
    'id': fields.Integer,
    'name': fields.String,
    'disabled': fields.Boolean,
    'operator_id': fields.Integer,
    'operator_name': fields.String,
    'operate_time': fields.DateTime(),
    'description': fields.String,
}


# API fields
#
utility_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(utility_record_field),
}

utility_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(utility_record_field)),
}
