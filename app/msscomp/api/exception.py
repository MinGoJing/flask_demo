#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Desc    :   provide exception definitions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/22 06:31, MinGo
          1. Created.

'''

# py


# common
from app.common.exception import APIException

# local
from .code import RET

# log
import logging
log = logging.getLogger("MSS")


class MsssAPIException(APIException):
    _ret_cls = RET

    def __init__(self, data=None, msg="", raw_data=None, lan="en"):
        APIException.__init__(self, data=data, msg=msg,
                              raw_data=raw_data, lan=lan)


class E0Exception(MsssAPIException):
    """
    @data : ()
    """
    result_code = RET.E_
    msg = ('haha')
