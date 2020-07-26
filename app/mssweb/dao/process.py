#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   process.py
@Desc    :   provide process db processors
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/18 11:46, MinGo
          1. Created.

'''

# py


# common
from app.common.db import base_db_update_model

# model
from app.models import MsswProces

# export
__all__ = [
    'process_processor',
    'MsswProces'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class process_processor(base_db_update_model):
    _entity_cls = MsswProces
    _null_supported_filter_attrs = []
    _key_2_db_attr_map = {}
