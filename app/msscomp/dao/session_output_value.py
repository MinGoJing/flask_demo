#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_output_value.py
@Desc    :   provide session output values
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/24 05:56, MinGo
          1. Created.

'''

# py


# common
from app.common.db import base_db_processor

# model
from app.models import MsssSessionOutputValue

# export
__all__ = [
    'session_output_value_processor',
    'MsssSessionOutputValue'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class session_output_value_processor(base_db_processor):
    _entity_cls = MsssSessionOutputValue
    _null_supported_filter_attrs = []
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    # Otherwise, default to leftjoin
    _ex_join_rules_from_db_key = {}
    _unique_user_key_list = ["session_output_id", "index"]
    _key_2_db_attr_map = {
        "session_output_id": "fk_session_output_id",
    }
