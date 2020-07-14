#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide user defined db process
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/20 05:29, MinGo
          1. Created.

'''

# py
from os import path

# export
from .pub_dict import *
from .utility import *


g_init_done = False
if (not g_init_done):
    from app.common import init_db_processors
    CUR_FOLDER_PATH = path.dirname(path.abspath(__file__))
    init_db_processors(CUR_FOLDER_PATH)
    g_init_done = True
