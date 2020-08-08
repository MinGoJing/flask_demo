#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   func.py
@Desc    :   provide basic functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/14 05:27, MinGo
          1. Created.

'''

# py
import copy
import platform

# local
from .obj import mgt_c_object
from .exc import SubFeatureFilterTypeNotSupportException
from .exc import SubFeatureFilterKeyNotFoundException
from .exc import SubFeatureDictIndexKeyNotFoundException
from .exc import SubFeatureDictIndexKeyValueRepeatException
from .exc import SubFeatureDictMultiTargetValueException

# log
import logging
log = logging.getLogger('MSS')


# export
__all__ = [
    "SLASH",
    "sub_feature_filter"
]


# SLASH
SLASH = None
if (SLASH is None):
    if (platform.system() == "Windows"):
        SLASH = "\\"
    else:
        SLASH = "/"


def sub_feature_dict(targets, idx_key, tar_key_path=[], b_strict=True):
    if (not idx_key):
        raise Exception()

    if (not targets):
        return {}

    if (not isinstance(targets, (list, tuple))):
        targets = [targets]

    #
    ret_dict = {}
    if (isinstance(targets[0], dict)):
        for item in targets:
            # source key
            try:
                idx_v = item[idx_key]
                if (idx_v in ret_dict):
                    raise SubFeatureDictIndexKeyValueRepeatException(
                        (idx_key, idx_v))
            except KeyError as e:
                log.error(e)
                if (b_strict):
                    raise SubFeatureDictIndexKeyNotFoundException(idx_key)
                else:
                    continue

            # target attr
            tar_attr_list = sub_feature_filter(
                [item], key_path=tar_key_path, b_strict=b_strict)

            if (1 != len(tar_attr_list)):
                if (b_strict):
                    raise SubFeatureDictMultiTargetValueException(
                        str(tar_key_path))
                else:
                    # key : <empty>, continue
                    log.error("No target value found from key path<%s>" %
                              (str(tar_key_path)))
                    continue

            ret_dict[idx_v] = tar_attr_list[0]

    elif (isinstance(targets[0], mgt_c_object)):
        for item in targets:
            # source key
            try:
                idx_v = getattr(item, idx_key)
                if (idx_v in ret_dict):
                    raise SubFeatureDictIndexKeyValueRepeatException(
                        (idx_key, idx_v))
            except KeyError as e:
                log.error(e)
                if (b_strict):
                    raise SubFeatureDictIndexKeyNotFoundException(idx_key)
                else:
                    continue

            # target attr
            tar_attr_list = sub_feature_filter(
                [item], key_path=tar_key_path, b_strict=b_strict)

            if (1 != len(tar_attr_list)):
                if (b_strict):
                    raise SubFeatureDictMultiTargetValueException(
                        str(tar_key_path))
                else:
                    # key : <empty>, continue
                    log.error("No target value found from key path<%s>" %
                              (str(tar_key_path)))
                    continue

            ret_dict[idx_v] = tar_attr_list[0]
    else:
        raise SubFeatureFilterTypeNotSupportException(str(type(targets[0])))

    return ret_dict


def sub_feature_filter(targets, key_path=[], b_strict=True):
    if (not targets):
        return []

    if (not isinstance(targets, (list, tuple))):
        targets = [targets]

    if (not key_path):
        return targets

    #
    current_list = targets
    i = 0

    if (isinstance(targets[0], dict)):
        while (i < len(key_path)):
            fetch_key = key_path[i]
            try:
                current_list = _dict_list_single_key_filter(
                    current_list, fetch_key, b_strict)
            except KeyError as e:
                log.error(e)
                raise SubFeatureFilterKeyNotFoundException(str(key_path))
            i += 1
    elif (isinstance(targets[0], mgt_c_object)):
        while (i < len(key_path)):
            fetch_key = key_path[i]
            try:
                current_list = _obj_list_single_key_filter(
                    current_list, fetch_key, b_strict)
            except KeyError as e:
                log.error(e)
                raise SubFeatureFilterKeyNotFoundException(str(key_path))
            i += 1
    else:
        raise SubFeatureFilterTypeNotSupportException(str(type(targets[0])))

    return current_list


def _obj_list_single_key_filter(list_to_filter: list, key, b_strict=True):
    if (not list_to_filter):
        return []

    handel_list = copy.deepcopy(list_to_filter)
    while (isinstance(handel_list[0], (list, tuple))):
        expend_list = []
        for items in handel_list:
            expend_list += items
        handel_list = expend_list

    if (b_strict):
        return [getattr(item, key) for item in handel_list]
    return [getattr(item, key) for item in handel_list if hasattr(item, key)]


def _dict_list_single_key_filter(list_to_filter: list, key, b_strict=True):
    if (not list_to_filter):
        return []

    handel_list = copy.deepcopy(list_to_filter)
    while (isinstance(handel_list[0], (list, tuple))):
        expend_list = []
        for items in handel_list:
            expend_list += items
        handel_list = expend_list

    if (b_strict):
        return [item[key] for item in handel_list]
    return [item[key] for item in handel_list if (key in item)]


if ("__main__" == __name__):
    ret_list = sub_feature_filter({"name": "jsdkf"}, ["name"])
    print("done.")
