#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   code.py
@Desc    :   provide basic result code
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/18 21:48, MinGo
          1. Created.

'''

# py


"""
****************************************************************************
 * Const & Basic Function Define!
****************************************************************************
"""
MGC_RESULT_FAIL_FLAG = 0x80000000


def FAIL_CODE(__layer_base__, __module_base__, __http_code__, __module_code__):
    return (MGC_RESULT_FAIL_FLAG | ((__layer_base__)+(__module_base__)+(__http_code__ << 8)+(__module_code__)))


def SUCCESS_CODE(__layer_base__, __module_base__, __http_code__, __module_code__):
    return (__layer_base__)+(__module_base__)+(__http_code__ << 8)+(__module_code__)


def OK(hr):
    if (not isinstance(hr, str)):
        return (hr == 0)
    else:
        return (int(hr, 16) == 0)


def SUCCEEDED(hr):
    if (not isinstance(hr, str)):
        return ((hr & MGC_RESULT_FAIL_FLAG) == 0)
    else:
        return ((int(hr, 16) & MGC_RESULT_FAIL_FLAG) == 0)


def FAILED(hr):
    if (not isinstance(hr, str)):
        return ((hr & MGC_RESULT_FAIL_FLAG) != 0)
    else:
        return ((int(hr, 16) & MGC_RESULT_FAIL_FLAG) != 0)


"""****************************************************************************
 * Layer Codes Area Define!
 * Use the lowest level that the error occurs
****************************************************************************"""
PLF_LAYER = 0x00000000
SVC_LAYER = 0x03000000
APP_LAYER = 0x06000000
API_LAYER = 0x0A000000
TRD_LAYER = 0x0D000000


"""****************************************************************************
 * Module Codes Area Define!
****************************************************************************"""
##=========================================================##
# Modules base
##=========================================================##
MODULE_DB = 0x0000000
MODULE_ORM = 0x0100000
MODULE_SYS = 0x0200000
MODULE_REQ = 0x0300000


class RET(object):
    ##=========================================================##
    # TimeOut Codes Area!
    ##=========================================================##
    TIMEOUT_IMMEDIATE = 0,
    TIMEOUT_INFINITY = 0xFFFFFFFF,

    ##=========================================================##
    # PLF - System
    ##=========================================================##
    S_OK = 0
    S_FALSE = 1

    E_FAIL = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x01))
    E_NO_IMPL = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x04))
    E_INVALID_ARG = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x05))
    E_BAD_PARAMETER = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x06))
    E_TIMEOUT = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x07))
    E_BUFFER_OVERFLOW = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x08))
    E_NONE_INPUT_PARAMETER = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x09))
    E_INDEX_OUT_OF_RANGE = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x0a))
    E_TYPE_FORMAT_CAST_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_SYS, 0x500, 0x0b))
    E_UNEXPECTED = (0x82F500FF)

    ##=========================================================##
    # PLF - ORM
    ##=========================================================##
    E_ORM_ENTITY_NOT_FOUND_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x500, 0x01))
    E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x500, 0x02))
    E_ENTITY_AUTO_JOIN_FAILED = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x500, 0x03))
    E_ENTITY_BACKREF_NOT_FOUND_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x500, 0x04))

    E_ENTITY_UPDATE_UNIQUE_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x400, 0x01))
    E_UPDATE_ENTITY_NOT_FOUND_ERROR = \
        (FAIL_CODE(PLF_LAYER, MODULE_ORM, 0x400, 0x02))

    S_DELETE_ENTITY_NOT_FOUND = \
        (SUCCESS_CODE(PLF_LAYER, MODULE_ORM, 0x200, 0x01))

    ##=========================================================##
    # API - request
    ##=========================================================##
    E_REQUEST_BAD_PARAMETER = \
        (FAIL_CODE(API_LAYER, MODULE_REQ, 0x400, 0x01))

    _info_dict = {
        # PLF - SYS
        S_OK: {
            "en": "S_OK",
            "zh-cn": "成功"},
        S_FALSE: {
            "en": "S_FALSE",
            "zh-cn": "操作完毕，假值返回"},

        E_TYPE_FORMAT_CAST_ERROR: {
            "en": "E_TYPE_FORMAT_CAST_ERROR",
            "zh-cn": "E_TYPE_FORMAT_CAST_ERROR(zh-cn)"},
        E_FAIL: {
            "en": "E_FAIL",
            "zh-cn": "E_FAIL(zh-cn)"},
        E_NO_IMPL: {
            "en": "E_NO_IMPL",
            "zh-cn": "E_NO_IMPL(zh-cn)"},
        E_INVALID_ARG: {
            "en": "E_INVALID_ARG",
            "zh-cn": "E_INVALID_ARG(zh-cn)"},
        E_BAD_PARAMETER: {
            "en": "E_BAD_PARAMETER",
            "zh-cn": "E_BAD_PARAMETER(zh-cn)"},
        E_TIMEOUT: {
            "en": "E_TIMEOUT",
            "zh-cn": "E_TIMEOUT(zh-cn)"},
        E_BUFFER_OVERFLOW: {
            "en": "E_BUFFER_OVERFLOW",
            "zh-cn": "E_BUFFER_OVERFLOW(zh-cn)"},
        E_NONE_INPUT_PARAMETER: {
            "en": "E_NONE_INPUT_PARAMETER",
            "zh-cn": "E_NONE_INPUT_PARAMETER(zh-cn)"},
        E_INDEX_OUT_OF_RANGE: {
            "en": "E_INDEX_OUT_OF_RANGE",
            "zh-cn": "E_INDEX_OUT_OF_RANGE(zh-cn)"},
        E_UNEXPECTED: {
            "en": "E_UNEXPECTED",
            "zh-cn": "未预料的错误"},


        # PLF ORM
        #
        E_ORM_ENTITY_NOT_FOUND_ERROR: {
            "en": "E_ORM_ENTITY_NOT_FOUND_ERROR",
            "zh-cn": "数据库表对象未找到"},
        E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR: {
            "en": "E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR",
            "zh-cn": "ORM BaseDbProcessor生成JOIN语句时，JOIN条件超过支持的数量[2]"},
        E_ENTITY_AUTO_JOIN_FAILED: {
            "en": "E_ENTITY_AUTO_JOIN_FAILED",
            "zh-cn": "ORM 自动生成JOIN规则失败"},
        E_ENTITY_BACKREF_NOT_FOUND_ERROR: {
            "en": "E_ENTITY_BACKREF_NOT_FOUND_ERROR",
            "zh-cn": "ORM 数据表backref映射丢失"},
        E_ENTITY_UPDATE_UNIQUE_ERROR: {
            "en": "E_ENTITY_UPDATE_UNIQUE_ERROR",
            "zh-cn": "数据库表对象更新唯一性校验失败"},
        E_UPDATE_ENTITY_NOT_FOUND_ERROR: {
            "en": "E_UPDATE_ENTITY_NOT_FOUND_ERROR",
            "zh-cn": "对象更新失败，ID无效"},

        S_DELETE_ENTITY_NOT_FOUND: {
            "en": "S_DELETE_ENTITY_NOT_FOUND",
            "zh-cn": "对象删除未完成，ID无效"},

        # API REQ
        #
        E_REQUEST_BAD_PARAMETER: {
            "en": "E_ENTITY_UPDATE_UNIQUE_ERROR",
            "zh-cn": "Request请求参数有误"},

        None: {
            "en": "<RET NOT FOUND>",
            "zh-cn": "<未知返回值>"}
    }

    @staticmethod
    def INFO(code, lan="en"):
        return RET._info_dict.get(code, {"en": "<RET NOT FOUND>", "zh-cn": "<未知返回值>"}).get(lan).replace('_', " ")
