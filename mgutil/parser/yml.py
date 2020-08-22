#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   yml.py
@Desc    :   provide yaml config parser
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/14 05:29, MinGo
          1. Created.

'''

# py
import re
import yaml
from os import path


# base
from ..base.obj import mgt_c_object


# export
__all__ = ["mgt_c_yaml_object"]


class mgt_c_yaml_object(mgt_c_object):

    def __init__(self, json_cfg, file_encoding='utf-8'):
        config_json = {}
        if (isinstance(json_cfg, dict)):
            config_json = json_cfg
        elif (isinstance(json_cfg, str)):
            if (not path.exists(json_cfg)):
                print(
                    "json config file[%s] NOT exists on local disk." % json_cfg)
                return
            else:
                f_obj = open(json_cfg, encoding=file_encoding)
                config_json = yaml.load(f_obj)

        update_reference_4_json(config_json)

        mgt_c_object.__init__(self, config_json, True)

    def test_attr(self, *keys):
        fetch_obj = self
        for i in range(len(keys)):
            key = keys[i]
            if (isinstance(fetch_obj, mgt_c_object)):
                fetch_obj = getattr(fetch_obj, key)
            else:
                return False

        return True


def update_reference_4_json(json_obj):

    def _get(json_obj, ref_path):
        fetch_obj = json_obj
        for node in ref_path:
            if (not isinstance(fetch_obj, dict)):
                return
            fetch_obj = fetch_obj.get(node, {})
        return fetch_obj
        # return reduce(lambda d, k: d[k], ref_path, json_obj)

    def _replace(obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                _replace(v)
            if isinstance(v, str):
                match_keys = re.findall(r'\$\{([a-zA-Z0-9_\.]+)\}', v)
                if match_keys:
                    for match_key in match_keys:
                        if (not match_key.count('.')):
                            if (match_key in obj):
                                replace_v = obj[match_key]
                            elif (match_key in json_obj):
                                replace_v = json_obj[match_key]
                            else:
                                return
                        else:
                            ref_path = match_key.split('.')
                            replace_v = _get(json_obj, ref_path)

                        v = re.sub(r'\$\{(%s)\}' %
                                   (match_key), str(replace_v), v)
                        obj[k] = v

    _replace(json_obj)
    return json_obj
