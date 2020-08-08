#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   code.py
@Desc    :   provide result codes
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/22 06:29, MinGo
          1. Created.

'''

# py

# common RET
from app.common import RET as RET_COMMON


# ****************************************************************************
#   Layer Codes Area Define!
#   Use the lowest level that the error occurs
# ****************************************************************************
from app.common.code import PLF_LAYER
from app.common.code import SVC_LAYER
from app.common.code import APP_LAYER
from app.common.code import API_LAYER
from app.common.code import TRD_LAYER


# ***************************************************************************
#  Const & Basic Function Define!
# ***************************************************************************
from app.common.code import FAIL_CODE
from app.common.code import SUCCESS_CODE


"""****************************************************************************
 * Module Codes Area Define!
****************************************************************************"""
##=========================================================##
# Modules base
##=========================================================##
MODULE_COMP = 0x1000000


class RET(object):
    ##=========================================================##
    # API - system
    ##=========================================================##
    E_ = \
        (FAIL_CODE(API_LAYER, MODULE_COMP, 0x500, 0x01))

    _info_dict = {
        # API - SYS
        E_: {
            "en": "E_",
            "zh-cn": "wei"},

        None: {
            "en": "<RET NOT FOUND>",
            "zh-cn": "<未知返回值>"}
    }

    @staticmethod
    def INFO(code, lan="en"):
        return RET._info_dict.get(code, RET_COMMON.INFO(code)).get(lan).replace('_', ' ')
