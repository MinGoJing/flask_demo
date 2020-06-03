#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide mssweb module API & Resource
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/05/26 07:02, MinGo
          1. Created.

'''

# py
import os

# flask restful
from flask_restful import Api


# api error
from .api.error import errors
# api resource
from .api.resource.pub_dict import pub_dict
from .api.resource.pub_dict import pub_dict_s


def init_module(api):
    # merge exceptions
    api.errors.update(errors)

    # add resource
    api.add_resource(pub_dict, "/dict/<dict_id>", endpoint="dict")
    api.add_resource(pub_dict_s, "/dicts", endpoint="dicts")