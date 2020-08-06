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

# app
from app import PROJ_HOME_PATH

# export
from .pub_dict import *
from .utility import *
from .program import *
from .task import *
from .task_input import *
from .task_output import *

g_init_done = False
if (not g_init_done):
    from app.common import init_db_processors
    CUR_FOLDER_PATH = path.dirname(path.abspath(__file__))
    init_db_processors(CUR_FOLDER_PATH, "app.mssweb.dao")
    g_init_done = True
