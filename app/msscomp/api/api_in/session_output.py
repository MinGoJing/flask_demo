#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_output.py
@Desc    :   provide session output parser
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/24 05:25, MinGo
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
    'session_output_add_par',
    'session_output_put_par',
    'session_output_get_par',
    'session_output_dd_par'
]


# session_output
# add
session_output_add_par = RequestParser()
session_output_add_par.add_argument('name',
                                    type=str, required=True,
                                    help='Parameter group name. (Required)')
session_output_add_par.add_argument('index',
                                    type=str, required=True,
                                    help='Parameter group index in session. (Required)')
session_output_add_par.add_argument('session_id',
                                    type=str, required=True,
                                    help='session_id. (Required)')
session_output_add_par.add_argument('note',
                                    type=str,
                                    help='note.')
# put
session_output_put_par = session_output_add_par.copy()
session_output_put_par.add_argument('id',
                                    type=int, required=True,
                                    help='ID. (Required)')
session_output_put_par.replace_argument('name',
                                        type=str,
                                        help='Parameter group name.')
session_output_put_par.replace_argument('index',
                                        type=str,
                                        help='Parameter group index in session.')
session_output_put_par.replace_argument('session_id',
                                        type=str,
                                        help='session_id. (Required)')
# get
session_output_get_par = CommonFilterParser()  # page_*, ids, disabled
session_output_get_par.add_argument('id',
                                    type=int,
                                    help='ID = ?')
session_output_get_par.add_argument('output_group_name',
                                    type=str,
                                    help='output_group_name = ?')
session_output_get_par.add_argument('session_id',
                                    type=str,
                                    help='session_id.')
session_output_get_par.add_argument('instance_id',
                                    type=str,
                                    help='instance_id.')

# delete & disable
session_output_dd_par = CommonDisableParser()  # id, ids, desc
