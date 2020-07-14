#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utility.py
@Desc    :   provide utility API input parser
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/12 22:18, MinGo
          1. Created.

'''

# py


# flask
from flask_restful.reqparse import RequestParser

# common
from app.common.restful_parser import CommonFilterParser
from app.common.restful_parser import CommonDisableParser

# export
__all__ = [
    'utility_add_par',
    'utility_put_par',
    'utility_get_par',
    'utility_dd_par'
]


# utility_parser
# add
utility_add_par = RequestParser()
utility_add_par.add_argument('name',
                             type=str, required=True,
                             help='Enum name. (Required)')
utility_add_par.add_argument('dict_utility_main_group_id',
                             type=int, required=True,
                             help='Utility main group ID. (Required)')
utility_add_par.add_argument('dict_utility_sub_group_id',
                             type=int, required=True,
                             help='Utility sub group ID. (Required)')
utility_add_par.add_argument('description',
                             type=str,
                             help='Note.')
# put
utility_put_par = utility_add_par.copy()
utility_put_par.add_argument('id',
                             type=int, required=True,
                             help='ID. (Required)')
utility_put_par.replace_argument('name',
                                 type=str,
                                 help='Enum name.')
utility_put_par.replace_argument('dict_utility_main_group_id',
                                 type=int,
                                 help='Utility main group ID.')
utility_put_par.replace_argument('dict_utility_sub_group_id',
                                 type=int,
                                 help='Utility sub group ID.')
utility_put_par.replace_argument('description',
                                 type=str,
                                 help='Note.')
# get
utility_get_par = CommonFilterParser()  # page, ids, disabled
utility_get_par.add_argument('id',
                             type=int,
                             help='ID = ?')
utility_get_par.replace_argument('name',
                                 type=str,
                                 help='name = ?(str)')
utility_get_par.replace_argument('dict_utility_main_group_name',
                                 type=str,
                                 help='Utility main group Name.')
utility_get_par.replace_argument('dict_utility_sub_group_name',
                                 type=str,
                                 help='Utility sub group Name.')

# delete & disable
utility_dd_par = CommonDisableParser()
