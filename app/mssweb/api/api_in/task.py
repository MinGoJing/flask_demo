#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task.py
@Desc    :   provide task parsers
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/30 07:07, MinGo
          1. Created.

'''

# py


# flask
from flask_restful.reqparse import RequestParser

# common
from app.common.restful_fields import *
from app.common.restful_parser import CommonFilterParser
from app.common.restful_parser import CommonDisableParser

# export
__all__ = [
    'task_add_par',
    'task_put_par',
    'task_get_par',
    'task_dd_par'
]


# task
# add
task_add_par = RequestParser()
task_add_par.add_argument('fk_program_id',
                          type=int, required=True,
                          location=['form', 'json'],
                          help='program_id. (Required)')
task_add_par.add_argument('processor_id',
                          type=int, required=True,
                          location=['form', 'json'],
                          help='processor_id. (Required)')
task_add_par.add_argument('task_inputs',
                          type=dict, required=True,  # field: <list:task_input>
                          location=['form', 'json'],
                          help='task_inputstask inputs. (Required)')
task_add_par.add_argument('note',
                          type=str,
                          location=['form', 'json'],
                          help='note. (Required)')

# put
task_put_par = RequestParser()
task_put_par.remove_argument("fk_program_id")
task_put_par.add_argument('status',
                          type=str, required=True,
                          location=['form', 'json'],
                          help='task status. (Required)')


# get
task_get_par = CommonFilterParser()  # page_*, ids, disabled
task_get_par.add_argument('id',
                          type=int,
                          location=['args'],
                          help='Task ID = ?')
task_get_par.add_argument('processor_id',
                          type=int,
                          help='processor user id = ?')

# delete & disable
task_dd_par = CommonDisableParser()  # id, ids, desc
