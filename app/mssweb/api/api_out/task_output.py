#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_output.py
@Desc    :   provide task output fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/30 23:41, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# export
__all__ = [
    'task_output_record_field',
    'task_output_record_fields',
    'task_output_records_fields'
]


# local fields
#
task_output_record_field = {
    'id': fields.Integer,
    'fk_task_id': fields.Integer,
    'module_name': fields.String,
    'key': fields.String,
    'index': fields.Integer,
    'data_type': fields.Integer,
    'value': fields.String,
}


# API fields
#
task_output_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(task_output_record_field),
}

task_output_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(task_output_record_field)),
}
