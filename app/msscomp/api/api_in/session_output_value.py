#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_output_value.py
@Desc    :   provide session output value fields
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/24 06:12, MinGo
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
    'session_output_value_add_par',
    'session_output_value_put_par',
    'session_output_value_get_par',
    'session_output_value_dd_par'
]


# session_output_value
# add
session_output_value_add_par = RequestParser()
session_output_value_add_par.add_argument('session_output_id',
                                          type=str, required=True,
                                          help='session_output_id. (Required)')
session_output_value_add_par.add_argument('key',
                                          type=str, required=True,
                                          help='output key. (Required)')
session_output_value_add_par.add_argument('index',
                                          type=str, required=True,
                                          help='output index. (Required)')
session_output_value_add_par.add_argument('data_type',
                                          type=str, required=True,
                                          help='output data_type. (Required)')
session_output_value_add_par.add_argument('v1',
                                          type=str,
                                          help='output v1.')
session_output_value_add_par.add_argument('v2',
                                          type=str,
                                          help='output v2 relation with v1.')
session_output_value_add_par.add_argument('v3',
                                          type=str,
                                          help='output v3 in list or complex value.')


# put
session_output_value_put_par = RequestParser()
# get
session_output_value_get_par = CommonFilterParser()  # page_*, ids, disabled
session_output_value_get_par.add_argument('id',
                                          type=int,
                                          help='ID = ?')
session_output_value_get_par.add_argument('session_output_name',
                                          type=str,
                                          help='session_output_name = ?')

# delete & disable
session_output_value_dd_par = CommonDisableParser()  # id, ids, desc
