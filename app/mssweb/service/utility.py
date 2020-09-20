#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utility.py
@Desc    :   provide utility service functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/07/15 21:37, MinGo
          1. Created.

'''

# py

# dao
from app.mssweb.dao import utility_processor


def utility_s_filter(filter_param, joined_keys=[]):
    if (filter_param.get("utility_main_group_name")):
        filter_param["utility_main_group.name"] = filter_param["utility_main_group_name"]
        filter_param.pop("utility_main_group_name")
    if (filter_param.get("utility_sub_group_name")):
        filter_param["utility_main_group.name"] = filter_param["utility_sub_group_name"]
        filter_param.pop("utility_sub_group_name")

    return utility_processor.get(filter_param)
    # , order_by = ["utility_main_group.id", "-utility_sub_group.id"], joined_keys=joined_keys
