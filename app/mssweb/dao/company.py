#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   company.py
@Desc    :   provide company processors
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/08/16 23:10, MinGo
          1. Created.

'''

# py


# common
from app.common.db import base_db_init_processor
from app.common.db import base_db_update_processor

# model
from app.models import Company

# export
__all__ = [
    'company_processor',
    'company_init_processor',
    'Company'
]


# keep class name starts with FILENAME_BASE, and connected with _processor
#
class company_processor(base_db_update_processor):
    _entity_cls = Company
    _null_supported_filter_db_attrs = []
    # Use db unique settings as default.
    #   You can define it here if forgot this in db design.
    _unique_user_key_list = ["name"]
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


class company_init_processor(company_processor, base_db_init_processor):
    _entity_cls = Company
    _null_supported_filter_db_attrs = []
    # Use db unique settings as default.
    #   You can define it here if forgot this in db design.
    _unique_user_key_list = ["name"]
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

    # init area
    _table_dependences = []
    # @str1 : {
    #   'remote_table': @str2,
    #   'fetch_key': @str3,
    #   'remote_ref_key': @str4
    # }
    #   @str1: local reference key
    #   @str2: reference table name
    #   @str3: reference table's fetch key
    #   @str4: reference table's reference key, (not given == 'id')
    _reference_key_2_fetch_target = {}
    _autogen_keys = []
    # the columns displayed to user is usually friendly
    #   we should transform them 2 processor key
    _friend_key_2_key_dict = {}
