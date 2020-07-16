# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utility_dao.py
@Desc    :   provide utility db model process
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/11 19:30, MinGo
          1. Created.

'''

# py

# common
from app.common.db import base_db_update_model

# model
from ..model import MsswUltility

# export
__all__ = [
    "utility_processor",
    "MsswUltility"
]


class utility_processor(base_db_update_model):
    _entity_cls = MsswUltility
    _null_supported_filter_attrs = []
    _key_2_db_attr_map = {
        "utility_main_group_id": "fk_dict_utility_main_group_id",
        "utility_sub_group_id": "fk_dict_utility_sub_group_id",
        "utility_main_group": "fk_dict_utility_main_group",
        "utility_sub_group": "fk_dict_utility_sub_group"
    }
