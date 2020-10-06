#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session services
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/27 23:00, MinGo
          1. Created.

'''

# py

# dao

from app.msscomp.dao import session_processor


def session_s_filer(filter_param={}, joined_keys=[]):
    if (filter_param.get("input_name")):
        filter_param["session_inputs.name"] = filter_param["input_name"]
        filter_param.pop("input_name")

    return session_processor.get(filter_param, joined_keys=joined_keys)
