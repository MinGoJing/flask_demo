#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session processors
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/23 06:23, MinGo
          1. Created.

'''

# py

# common
from app.common.db import base_db_update_processor

# model
from app.models import MsssSession

# export
__all__ = [
    'session_processor',
    'MsssSession'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class session_processor(base_db_update_processor):
    _entity_cls = MsssSession
    _null_supported_filter_attrs = []
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    # This is useful if there is NO foreign key settings in DB schema
    # @format:
    #   "$(db_foreign_key)": {
    #       "type": "outerjoin",            # choices = ["outerjoin", "join"]
    #       "remote_entity_cls": PubDict,   # relation entity class, the auto generated ones
    #       "remote_db_key": "id",          # remote entity key to be joined
    #       "other_rules": [(local_db_key, remote_db_key), ()]
    #                                       # If the join rule is a bit more complex, add extra
    #                                       # rules here. Check if we have implemented this while
    #                                       # doing gen_query().
    #   }
    _ex_join_rules_from_db_key = {
        "msss_session_inputs": {
            "type": "join",
            "remote_entity_cls": MsssSession,
            "remote_db_key": "id",
            "other_rules": []
        }
    }
    _unique_user_key_list = ["instance_id"]
    _key_2_db_attr_map = {
        "session_inputs": "msss_session_inputs",
        "session_outputs": "msss_session_outputs"
    }
    _entity_relation_backref_db_attr_list = []
