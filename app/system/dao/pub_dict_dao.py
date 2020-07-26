#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pub_dict_dao.py
@Desc    :   provide pub dict model process.
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/05/10 15:01, MinGo
          1. Created.

'''

# py

# common
from app.common.db import base_db_processor

# model
from app.models import PubDict


class pub_dict_processor(base_db_processor):
    _entity_cls = PubDict
