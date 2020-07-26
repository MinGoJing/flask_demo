#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_input_value.py
@Desc    :   provide session input values
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
from app.models import MsssSessionInputValue

# export
__all__ = [
    'session_input_value_processor',
    'MsssSessionInputValue'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class session_input_value_processor(base_db_processor):
    _entity_cls = MsssSessionInputValue
    _null_supported_filter_attrs = []
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    _ex_join_rules_from_db_key = {}
    _unique_user_key_list = ["session_input_id", "index"]
    _key_2_db_attr_map = {
        "session_input_id": "fk_session_input_id",
    }
