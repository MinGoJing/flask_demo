#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task.py
@Desc    :   provide task fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/30 23:27, MinGo
          1. Created.

'''

# py


# flask
from flask_restful import fields

# local
from . task_input import task_input_record_field
from . task_output import task_output_record_field

# export
__all__ = [
    'task_record_field',
    'task_record_fields',
    'task_records_fields'
]


# local fields
#
task_record_field = {
    'id': fields.Integer,
    'fk_program_id': fields.Integer,
    'fk_program_config_id': fields.Integer,
    'status': fields.Integer,
    'processor_id': fields.Integer,
    'start_time': fields.DateTime(dt_format='iso8601'),
    'finish_time': fields.DateTime(dt_format='iso8601'),
    'note': fields.String,
    "task_inputs": fields.List(fields.Nested(task_input_record_field)),
    "task_outputs": fields.List(fields.Nested(task_output_record_field))
}


# API fields
#
task_record_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.Nested(task_record_field),
}

task_records_fields = {
    'msg': fields.String(default='ok'),
    'code': fields.Integer,
    'data': fields.List(fields.Nested(task_record_field)),
}
