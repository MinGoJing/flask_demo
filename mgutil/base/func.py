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
from .exc import SubFeatureFilterTypeNotSupportException
from .exc import SubFeatureFilterKeyNotFoundException
from .exc import SubFeatureDictIndexKeyNotFoundException
from .exc import SubFeatureDictIndexKeyValueRepeatException
from .exc import SubFeatureDictMultiTargetValueException
from .exc import SubFeatureMarshalTargetAttributeLostException

# log
import logging
log = logging.getLogger('UTIL')


# export
__all__ = [
    "SLASH",
    "is_data_rendered",
    "sub_feature_filter",
    "sub_feature_dict",
    "sub_feature_marshal"
]


# SLASH
SLASH = None
if (SLASH is None):
    if (platform.system() == "Windows"):
        SLASH = "\\"
    else:
        SLASH = "/"


def is_data_rendered(data, render_keys=["code", "data", "msg"]):
    if (isinstance(data, dict)):
        if (3 == len(set(render_keys) & set(data.keys()))):
            return True
    return False


def sub_feature_dict(targets, idx_key, tar_key_path=[], b_strict=True,
                     b_accpet_multi_target=False):
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

            if (not b_accpet_multi_target):
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
                ret_dict[idx_v] = tar_attr_list

    elif (isinstance(targets[0], object)):
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

            if (not b_accpet_multi_target):
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
                ret_dict[idx_v] = tar_attr_list
    else:
        raise SubFeatureFilterTypeNotSupportException(str(type(targets[0])))

    return ret_dict


def sub_feature_filter(targets, key_path=[], b_strict=True, b_end_attr_list_expend=True):
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
        while (i < len(key_path)-1):
            fetch_key = key_path[i]
            try:
                current_list = _dict_list_single_key_filter(
                    current_list, fetch_key, b_strict, b_list_expend=True)
            except KeyError as e:
                log.error(e)
                raise SubFeatureFilterKeyNotFoundException(
                    (str(key_path), fetch_key))
            i += 1
        # fetch ending attribute, do not expend list
        fetch_key = key_path[-1]
        current_list = _dict_list_single_key_filter(
            current_list, fetch_key, b_strict, b_list_expend=b_end_attr_list_expend)
    elif (isinstance(targets[0], object)):
        while (i < len(key_path)-1):
            fetch_key = key_path[i]
            try:
                current_list = _obj_list_single_key_filter(
                    current_list, fetch_key, b_strict, b_list_expend=True)
            except KeyError as e:
                log.error(e)
                raise SubFeatureFilterKeyNotFoundException(
                    (str(key_path), fetch_key))
            i += 1
        # fetch ending attribute, do not expend list
        fetch_key = key_path[-1]
        current_list = _obj_list_single_key_filter(
            current_list, fetch_key, b_strict, b_list_expend=b_end_attr_list_expend)
    else:
        raise SubFeatureFilterTypeNotSupportException(str(type(targets[0])))

    return current_list


def _obj_list_single_key_filter(list_to_filter: list, key,
                                b_strict=True, b_list_expend=True):
    if (not list_to_filter):
        return []

    handel_list = list_to_filter
    while (isinstance(handel_list[0], (list, tuple))):
        expend_list = []
        for items in handel_list:
            expend_list += items
        handel_list = expend_list

    if (b_strict):
        fetch_list = [getattr(item, key) for item in handel_list]
    fetch_list = [getattr(item, key)
                  for item in handel_list if hasattr(item, key)]

    if (b_list_expend):
        while (isinstance(fetch_list[0], (list, tuple))):
            expend_list = []
            for items in fetch_list:
                expend_list += items
            fetch_list = expend_list
    return fetch_list


def _dict_list_single_key_filter(list_to_filter: list, key,
                                 b_strict=True, b_list_expend=True):
    if (not list_to_filter):
        return []

    handel_list = list_to_filter
    while (isinstance(handel_list[0], (list, tuple))):
        expend_list = []
        for items in handel_list:
            expend_list += items
        handel_list = expend_list

    if (b_strict):
        fetch_list = [item[key] for item in handel_list]
    fetch_list = [item[key] for item in handel_list if (key in item)]

    if (b_list_expend):
        while (isinstance(fetch_list[0], (list, tuple))):
            expend_list = []
            for items in fetch_list:
                expend_list += items
            fetch_list = expend_list
    return fetch_list


def sub_feature_marshal(src_objs, src_match_key_path, src_marshal_end_key,
                        tar_objs, tar_match_key_path, tra_marshal_ending_keys,
                        b_strict=True):
    """
    @src_objs: source objects to be marshaled
        e.g. : groups: [
            "users": [
                {
                    "id": 1,
                    "name": "user_name1",
                    "product_set_id": 1
                },
                {
                    "id": 2,
                    "name": "user_name2",
                    "product_set_id": 2
                },
                {
                    "id": 3,
                    "name": "user_name3",
                    "product_set_id": 3
                },
                ...
            ]
        ]
    @src_match_key_path : source object key to match target objects
        e.g. : ["users", "product_set_id"]
    @src_marshal_end_key : source object marshal key to be added in the same parent key-path with source match key
        e.g. : "products" -> ["users", "products"]
    @tar_objs : source objects to be marshaled in
        e.g. : product_sets: [
            {
                "id": 1,
                "products": [
                    {
                    "id": 1,
                    "name": "product1"
                    },
                    {
                    "id": 2,
                    "name": "product2"
                    },
                    {
                    "id": 3,
                    "name": "product3"
                    },
                ]
            },
            ...
        ]
    @tar_match_key_path : target object key to match source object
        e.g. : ["id"]
    @tra_marshal_ending_keys : target object key to be marsheled in the same parent key-path with target match key
        e.g. : ["products", "name"] -> ["products", "name"]
    @b_strict : <boolean>
        if sub feature filtering should do strict key path check, refers to <any:sub_feature_filter>
    """
    # src_objs, src_match_key_path, src_marshal_end_key,
    # tar_objs, tar_match_key_path, tra_marshal_ending_keys
    if (not src_objs or not tar_objs or not src_match_key_path or not tar_match_key_path):
        return

    # prepare match_key_value : src_pre_match object dict
    #
    if (1 < len(src_match_key_path)):
        src_pre_match_objs = sub_feature_filter(
            src_objs, src_match_key_path[:-1], b_strict=b_strict)
    else:
        src_pre_match_objs = src_objs
    match_v_2_src_pre_match_obj_dict = sub_feature_dict(
        src_pre_match_objs, idx_key=src_match_key_path[-1], b_strict=b_strict)

    # parpare match_key_value : tar_pre_match marshal attribute dict
    #
    if (1 < len(tar_match_key_path)):
        tar_pre_match_objs = sub_feature_filter(
            tar_objs, tar_match_key_path[:-1], b_strict=b_strict)
    else:
        tar_pre_match_objs = tar_objs
    match_v_2_tar_marshal_attr_dict = sub_feature_dict(
        tar_pre_match_objs, idx_key=tar_match_key_path[-1],
        tar_key_path=tra_marshal_ending_keys, b_strict=b_strict,
        b_accpet_multi_target=True)

    # do marshal
    exc_match_v = None
    try:
        for match_v, src_pre_match_obj in match_v_2_src_pre_match_obj_dict.items():
            exc_match_v = match_v
            tar_marshal_attr = match_v_2_tar_marshal_attr_dict[match_v]
            src_pre_match_obj[src_marshal_end_key] = tar_marshal_attr
    except KeyError as e:
        log.error(e)
        if (b_strict):
            raise SubFeatureMarshalTargetAttributeLostException(
                (str(src_match_key_path), exc_match_v))
        else:
            src_pre_match_obj[src_marshal_end_key] = None

    return


# if ("__main__" == __name__):
#     obj = {
#         "name": "jsdkf",
#         "users": [
#             {
#                 "id": 12,
#                 "name": "user12",
#                 "number": "number12",
#                 "dps": {
#                     "id": 1,
#                     "name": "dp1"
#                 }
#             },
#             {
#                 "id": 13,
#                 "name": "user13",
#                 "number": "number13",
#                 "dps": {
#                     "id": 2,
#                     "name": "dp2"
#                 }
#             },
#             {
#                 "id": 14,
#                 "name": "user14",
#                 "number": "number14",
#                 "dps": {
#                     "id": 3,
#                     "name": "dp3"
#                 }
#             },
#         ]
#     }
#     # ret_list = sub_feature_filter(obj, ["users", "id"])
#     # ret_dict = sub_feature_dict(obj["users"], "id", ["dps", "name"])
#     # print(ret_list)
#     # print(ret_dict)

#     src_objs = [
#         {
#             "id": 1,
#             "users": [
#                 {
#                     "id": 1,
#                     "name": "user_name1",
#                     "product_set_id": 1
#                 },
#                 {
#                     "id": 2,
#                     "name": "user_name2",
#                     "product_set_id": 2
#                 },
#                 {
#                     "id": 3,
#                     "name": "user_name3",
#                     "product_set_id": 3
#                 }
#             ]
#         }
#     ]
#     tar_objs = [
#         {
#             "id": 1,
#             "products": [
#                 {
#                     "id": 1,
#                     "name": "product1"
#                 },
#                 {
#                     "id": 2,
#                     "name": "product2"
#                 },
#                 {
#                     "id": 3,
#                     "name": "product3"
#                 },
#             ]
#         },
#         {
#             "id": 2,
#             "products": [
#                 {
#                     "id": 21,
#                     "name": "product21"
#                 },
#                 {
#                     "id": 22,
#                     "name": "product22"
#                 },
#                 {
#                     "id": 23,
#                     "name": "product23"
#                 },
#             ]
#         },
#         {
#             "id": 3,
#             "products": [
#                 {
#                     "id": 31,
#                     "name": "product31"
#                 },
#                 {
#                     "id": 32,
#                     "name": "product32"
#                 },
#                 {
#                     "id": 33,
#                     "name": "product33"
#                 },
#             ]
#         }
#     ]
#     sub_feature_marshal(src_objs, ["users", "product_set_id"], "products",
#                         tar_objs, ["id"], ["products", "name"])
#     print(str(src_objs))

#     print("done.")
