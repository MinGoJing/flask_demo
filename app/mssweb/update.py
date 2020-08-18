#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   update.py
@Desc    :   provide db update process
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/08/13 22:18, MinGo
          1. Created.

'''

# py
from os import path
from datetime import datetime
from . dao import *

# util
from mgutil.parser.yml import mgt_c_yaml_object

# log
import logging
log = logging.getLogger('SYS')


def _init_round_1(yml_path):
    yml_obj = mgt_c_yaml_object(yml_path)
    datasheet = yml_obj.to_json()
    try:
        utility_init_processor.initialize(datasheet)
    except Exception as e:
        e = e


def db_update():
    cur_path = path.dirname(path.abspath(__file__))
    if (datetime.now() <= datetime.strptime("2020-08-31", "%Y-%m-%d")):
        _init_round_1(path.join(cur_path, "init_2020-08-13.yml"))
