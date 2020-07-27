#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide mingo demon web services
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/04/24 21:49, MinGo
          1. Created.

'''

# py


# flask restful
from flask_restful import Api


# api
from .api.resource import *


def init_module(api):
    # add resource
    pass
