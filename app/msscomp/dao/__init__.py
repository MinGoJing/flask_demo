#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide msscomp db processors
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/22 06:38, MinGo
          1. Created.

'''

# py
from os import path

# export
from .session import *
from .session_input import *
from .session_output import *


g_init_done = False
if (not g_init_done):
    from app.common import init_db_processors
    CUR_FOLDER_PATH = path.dirname(path.abspath(__file__))
    init_db_processors(CUR_FOLDER_PATH, 'app.msscomp.dao',
                       init_submod_list=None)
    g_init_done = True
