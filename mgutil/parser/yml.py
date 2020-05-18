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
import yaml
from os import path


# base
from ..base.obj import mgt_c_object_from_json


# export
__all__ = ["mgt_c_yaml_object"]


class mgt_c_yaml_object(mgt_c_object_from_json):

    def __init__(self, json_cfg):
        config_json = {}
        if (isinstance(json_cfg, dict)):
            config_json = json_cfg
        elif (isinstance(json_cfg, str)):
            if (not path.exists(json_cfg)):
                print(
                    "json config file[%s] NOT exists on local disk." % json_cfg)
                return
            else:
                f_obj = open(json_cfg)
                config_json = yaml.load(f_obj)

        mgt_c_object_from_json.__init__(self, config_json, True)

    def test_attr(self, *keys):
        fetch_obj = self
        for i in range(len(keys)):
            key = keys[i]
            if (isinstance(fetch_obj, mgt_c_object_from_json)):
                fetch_obj = getattr(fetch_obj, key)
            else:
                return False

        return True
