#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_input.py
@Desc    :   provide task input
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/30 23:43, MinGo
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
    'task_input_add_par',
    'task_input_put_par',
    'task_input_get_par',
    'task_input_dd_par'
]


# task_input
# add
task_input_add_par = RequestParser()
task_input_add_par.add_argument('fk_process_id',
                                type=int, required=True,
                                help='process_id. (Required)')
task_input_add_par.add_argument('module_name',
                                type=str,
                                help='module_name.')
task_input_add_par.add_argument('key',
                                type=str, required=True,
                                help='key. (Required)')
task_input_add_par.add_argument('index',
                                type=int, required=True,
                                help='index. (Required)')
task_input_add_par.add_argument('data_type',
                                type=int, required=True,
                                help='data_type. (Required)')
task_input_add_par.add_argument('value',
                                type=str,
                                help='value.')


# put
task_input_put_par = RequestParser()
task_input_put_par.add_argument('id',
                                type=int, required=True,
                                location=['args'],
                                help='Task ID. (Required)')
task_input_put_par.add_argument('value',
                                type=int, required=True,
                                location=['form'],
                                help='value.')
# get
task_input_get_par = RequestParser()

# delete & disable
task_input_dd_par = CommonDisableParser()  # id, ids, desc
