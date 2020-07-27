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
program_add_par.add_argument('name',
                             type=str, required=True,
                             help='. (Required)')
# put
program_put_par = program_add_par.copy()
program_put_par.add_argument('id',
                             type=int, required=True,
                             help='ID. (Required)')
program_put_par.replace_argument('name',
                                 type=str,
                                 help='.')
# get
program_get_par = CommonFilterParser()  # page_*, ids, disabled
program_get_par.add_argument('id',
                             type=int,
                             help='ID = ?')
program_get_par.add_argument('name',
                             type=str,
                             help='. = ?')

# delete & disable
program_dd_par = CommonDisableParser()  # id, ids, desc
