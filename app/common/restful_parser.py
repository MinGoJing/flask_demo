#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   restful_parser.py
@Desc    :   provide basic restful API arg parsers
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/05/27 22:26, MinGo
          1. Created.

'''

# py

# flask
from flask_restful.reqparse import RequestParser

# local
from .restful_fields import IntCombinedInStrField

# export
__all__ = [
    "PageFilterParser",
    "CommonFilterParser"
]


class PageFilterParser(RequestParser):

    def __init__(self):
        RequestParser.__init__(self)
        self.add_argument("page_index",
                          type=int, location=["args", "form"],
                          help="Page index, start from 1.")
        self.add_argument("page_size",
                          type=int, location=["args", "form"],
                          help="Page size, > 0.")


class CommonFilterParser(PageFilterParser):

    def __init__(self):
        PageFilterParser.__init__(self)
        self.add_argument("ids",
                          type=IntCombinedInStrField,
                          location=["args", "form"],
                          help=("A String, which is ID(int) combined by ','."))
        self.add_argument("disabled",
                          choices=[0, 1],
                          location=["args", "form"],
                          help=("disabled status, value choice. "
                                "1: disabled; 0: enabled;"))


class CommonDisableParser(RequestParser):

    def __init__(self):
        RequestParser.__init__(self)
        self.add_argument("id",
                          type=int,
                          location=["args", "form"],
                          help="ID")
        self.add_argument("ids",
                          type=IntCombinedInStrField,
                          location=["args", "form"],
                          help="IDs combined with ','")
        self.add_argument("desc",
                          type=str,
                          location=["args", "form"],
                          help="Disable or delete reason.")
