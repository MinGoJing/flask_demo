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


# api resource
from .api.program import program_s
from .api.program import program
from .api.pub_dict import pub_dict
from .api.pub_dict import pub_dict_s
from .api.utility import utility
from .api.utility import utility_s


def init_module(api):
    # add resource
    api.add_resource(pub_dict, "/dict/<dict_id>", endpoint="dict")
    api.add_resource(pub_dict_s, "/dicts", endpoint="dicts")
    api.add_resource(utility, "/utility/<utility_id>", endpoint="utility")
    api.add_resource(utility_s, "/utilitys", endpoint="utilitys")
    api.add_resource(program, '/program/<program_id>', endpoint='program')
    api.add_resource(program_s, '/programs', endpoint='programs')
