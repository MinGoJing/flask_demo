#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   program_dao.py
@Desc    :   provide program db model processor
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/11 20:20, MinGo
          1. Created.

'''

# py

# common
from app.common.db import base_db_update_model

# model
from app.models import MsswProgram

# export
__all__ = [
    'program_processor',
    'MsswProgram'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class program_processor(base_db_update_model):
    _entity_cls = MsswProgram
    _null_supported_filter_attrs = []
    _key_2_db_attr_map = {}
