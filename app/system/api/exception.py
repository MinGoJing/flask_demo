#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Desc    :   provide system exceptions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/26 10:07, MinGo
          1. Created.

'''

# py

# common
from app.common.exception import APIException

# local
from .code import RET


class SysAPIException(APIException):
    _ret_cls = RET
