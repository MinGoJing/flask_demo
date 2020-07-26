#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_parameter_value.py
@Desc    :   provide session parameter values
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
from app.common.db import base_db_update_model

# model
from app.models import MsssSessionParameterValue

# export
__all__ = [
    'session_parameter_value_processor',
    'MsssSessionParameterValue'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class session_parameter_value_processor(base_db_update_model):
    _entity_cls = MsssSessionParameterValue
    _null_supported_filter_attrs = []
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    # Otherwise, default to leftjoin
    _ex_join_rules_from_db_key = {}
    _unique_user_key_list = ["session_parameter_id", "index"]
    _key_2_db_attr_map = {
        "session_parameter_id": "fk_session_parameter_id",
    }
