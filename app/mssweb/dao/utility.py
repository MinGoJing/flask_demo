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
from app.common.db import base_db_update_processor
from app.common.db import base_db_inti_processor

# model
from app.models import MsswUltility, PubDict

# export
__all__ = [
    "utility_processor",
    "MsswUltility"
]


class utility_processor(base_db_update_processor):
    _entity_cls = MsswUltility
    _null_supported_filter_attrs = []
    # If NOT set, do inner_join if (foreign_key is NOT nullable) else left_join
    # Otherwise, default to leftjoin
    _ex_join_routes_from_db_key = {
        "fk_dict_main_group_id": {
            "type": "outerjoin",
            "remote_entity_cls": PubDict,
            "remote_db_key": "id",
            "other_rules": []
        }
    }
    _key_2_db_attr_map = {
        "utility_main_group_id": "fk_dict_utility_main_group_id",
        "utility_sub_group_id": "fk_dict_utility_sub_group_id",
        "utility_main_group": "fk_dict_utility_main_group",
        "utility_sub_group": "fk_dict_utility_sub_group"
    }


class utility_init_processor(utility_processor, base_db_init_processor):
    __table_dependences = ["pub_dict"]
    # @str1 : {"remote_table": @str2, "fetch_key": @str3, "remote_ref_key": @str4}
    #   @ref_key: local reference key
    #   @str2: reference table name
    #   @str3: reference table's fetch key
    #   @str4: reference table's reference key, not given => 'id'
    __reference_key_2_fetch_target = {}
    __autogen_keys = []
    __local_unique_fetch_keys = []  # except id
    __friend_key_2_key_dict = {}
