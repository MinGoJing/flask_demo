#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide init process
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :   
    1.0: 2020/01/11 18:46, MinGo
          1. Created.

'''

# py

# errors
from .error import errors

# export
from .db import *


def init_module(api):
    # merge exceptions
    # api.errors.update(errors)
    pass
