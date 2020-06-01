#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide base obj & function support
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/14 21:20, MinGo
          1. Created.

'''

# py
from .obj import mgt_c_object
from .obj import *


#
def fmt_json_result(data, msg="success"):
    if (not data):
        return {"data": data,
                "message": msg}

    if (isinstance(data, mgt_c_object)):
        return {"data": data.to_json(),
                "message": msg}
    elif (isinstance(data, (list, tuple))):
        data_list = mgt_c_object.parse_list(data)
        return {"data": data_list,
                "message": msg}
    else:
        return {"data": data,
                "message": msg}
