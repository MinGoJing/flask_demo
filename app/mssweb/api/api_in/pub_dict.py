#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pub_dict.py
@Desc    :   provide pub dict parsers
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/05/27 22:03, MinGo
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
    "dict_add_par",
    "dict_put_par",
    "dict_get_par",
    "dict_dd_par"
]


# pub dict parser
# add
dict_add_par = RequestParser()
dict_add_par.add_argument("category",
                          type=str, required=True,
                          help="Name of a group of Enum values. (Required)")
dict_add_par.add_argument("name",
                          type=str, required=True,
                          help="Enum name. (Required)")
dict_add_par.add_argument("disabled",
                          type=int, choices=[0, 1], default=0,
                          help=("disabled status, value choice. "
                                "1: disabled; 0: enabled;"))
dict_add_par.add_argument("note",
                          type=str,
                          help="Enum note.")
# put
dict_put_par = dict_add_par.copy()
dict_put_par.add_argument("id",
                          type=int, required=True,
                          help="Enum ID. (Required)")
dict_put_par.replace_argument("category",
                              type=str,
                              help="Name of a group of Enum values.")
dict_put_par.replace_argument("name",
                              type=str,
                              help="Enum name.")
# get
dict_get_par = CommonFilterParser()
dict_get_par.add_argument("id",
                          type=int,
                          help="ID = ?")
dict_get_par.replace_argument("category",
                              type=str,
                              help="category = ?")
dict_get_par.replace_argument("name",
                              type=str,
                              help="name = ?")

# del & dis
dict_dd_par = CommonDisableParser()
