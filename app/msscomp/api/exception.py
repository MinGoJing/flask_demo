#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Desc    :   provide exception definitions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/22 06:31, MinGo
          1. Created.

'''

# py


# common
from app.common.exception import APIException

# local
from .code import RET


class MsssAPIException(APIException):
    _ret_cls = RET
