#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   func.py
@Desc    :   provide basic useful functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/08/16 13:41, MinGo
          1. Created.

'''

# py


def is_data_rendered(data):
    if (isinstance(data, dict)):
        if (3 == len(set(["code", "data", "msg"]) & set(data.keys()))):
            return True
    return False
