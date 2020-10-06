#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_output.py
@Desc    :   provide task_output processor
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/31 06:25, MinGo
          1. Created.

'''

# py


# common
from app.common.db import base_db_update_processor

# model
from app.models import MsswTaskOutput

# export
__all__ = [
    'task_output_processor',
    'MsswTaskOutput'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class task_output_processor(base_db_update_processor):
    _entity_cls = MsswTaskOutput
    _null_supported_filter_db_attrs = []
    # Use db unique settings as default.
    #   You can define it here if forgot this in db design.
    _unique_user_key_list = []
    _key_2_db_attr_map = {}
    _default_value_map = {}
    # If NOT set, inner_join if foreign_key is NOT nullable else left_join
    # This is useful if there is NO foreign key settings in DB schema
    # @format:
    #   '$(db_foreign_key)': {
    #       'type': 'outerjoin',            # choices = ['outerjoin', 'join']
    #       'remote_entity_cls': PubDict,   # relation entity class, the auto generated ones
    #       'remote_db_key': 'id',          # remote entity key to be joined
    #       'other_rules': [(local_db_key, remote_db_key), ()]
    #                                       # If the join rule is a bit more complex, add extra
    #                                       # rules here. Check if we have implemented this while
    #                                       # doing gen_query().
    #   }
    _ex_join_rules_from_db_key = {}
