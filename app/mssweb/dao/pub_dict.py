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
from app.common.db import base_db_update_model

# model
from ..model import PubDict

# export
__all__ = [
    "pub_dict_processor",
    "PubDict"
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class pub_dict_processor(base_db_update_model):
    _entity_cls = PubDict
    _null_supported_filter_attrs = []
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    # Otherwise, default to leftjoin
    _ex_join_rules_from_db_key = {}
    _key_2_db_attr_map = {
        "id2": "id"
    }
