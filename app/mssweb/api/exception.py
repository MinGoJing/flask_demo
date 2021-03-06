#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Desc    :   provide system module associated exceptions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/05/20 05:31, MinGo
          1. Created.

'''

# py


# common
from app.common.exception import APIException

# local
from .code import RET


class MsswAPIException(APIException):
    _ret_cls = RET


class MsswUnexceptedException(MsswAPIException):
    """
    @data : 
        @ : entity name
    """
    code = RET.E_
    msg = ('')
