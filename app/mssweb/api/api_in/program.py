#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   program.py
@Desc    :   provide program parsers
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/27 07:07, MinGo
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
    'program_add_par',
    'program_put_par',
    'program_get_par',
    'program_dd_par'
]


# program
# add
program_add_par = RequestParser()
program_add_par.add_argument('utility_id',
                             type=int, required=True,
                             help='Utility ID. (Required)')
program_add_par.add_argument('version',
                             type=str, required=True,
                             help='version str like "0.0.1". (Required)')
program_add_par.add_argument('provider_employee_id',
                             type=int,
                             nullable=True,
                             help='provider employee ID.')
program_add_par.add_argument('description',
                             type=str,
                             help='description.')


# put
program_put_par = program_add_par.copy()
program_put_par.replace_argument('utility_id',
                                 type=int,
                                 help='Utility ID.')
program_put_par.replace_argument('version',
                                 type=str,
                                 help='version str like "0.0.1".')
program_put_par.replace_argument('provider_employee_id',
                                 type=int,
                                 store_missing=False,
                                 help='provider employee ID.')
# get
program_get_par = CommonFilterParser()  # page_*, ids, disabled
program_get_par.add_argument('name',
                             type=str,
                             help='Name = ?')

# delete & disable
program_dd_par = CommonDisableParser()  # id, ids, desc
