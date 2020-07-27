#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session api input
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/23 06:44, MinGo
          1. Created.

'''

# py


# flask
from flask_restful.reqparse import RequestParser

# common
from app.common.restful_fields import DateTimeStrField
from app.common.restful_parser import CommonFilterParser
from app.common.restful_parser import CommonDisableParser

# export
__all__ = [
    'session_add_par',
    'session_put_par',
    'session_get_par',
    'session_dd_par'
]


# session
# add
session_add_par = RequestParser()
session_add_par.add_argument('name', required=True,
                             type=str,
                             help='program_name. (Required)')
session_add_par.add_argument('note',
                             type=str,
                             help='note.')
session_add_par.add_argument('session_inputs', required=True,
                             type=dict, action="append",
                             help='session inputs.')
session_add_par.add_argument('session_parameters',
                             type=dict, action="append",
                             help='session parameters.')

# put
session_put_par = session_add_par.copy()
session_put_par.add_argument('id',
                             type=int, required=True,
                             help='ID. (Required)')
session_put_par.remove_argument('instance_id')
session_put_par.remove_argument('init_time')
# get
session_get_par = CommonFilterParser()  # page, ids, disabled
session_get_par.add_argument('id',
                             type=int,
                             help='ID = ?')
session_get_par.add_argument('instance_id',
                             type=int,
                             help='Instance ID = ?')
session_get_par.add_argument('input_name',
                             type=str,
                             help='session input name = ?')
session_get_par.add_argument('status',
                             type=int,
                             help='Session status[0: Created 1: Started 2: Crashed 3: UserCanceled 4: Finished].')


# delete & disable
session_dd_par = CommonDisableParser()  # id, ids, @staticmethod
session_dd_par.add_argument('instance_id',
                            type=int,
                            help='Instance ID = ?')
