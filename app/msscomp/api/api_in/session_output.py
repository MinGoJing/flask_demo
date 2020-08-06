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
# put
session_output_put_par = RequestParser()
# get
session_output_get_par = RequestParser()

# delete & disable
session_output_dd_par = RequestParser()
