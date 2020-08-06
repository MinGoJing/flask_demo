#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session app services
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/24 22:48, MinGo
          1. Created.

'''

# py
from ..dao import session_input_processor


def session_init(ss_id, params):
    #
    ss_inputs = params.get("session_inputs")

    # add inputs
    input_procs = [session_input_processor(obj) for obj in ss_inputs]
    for obj in input_procs:
        obj.session_id = ss_id
    rcd = session_input_processor.add_many(input_procs)

    return rcd


def session_process():
    # TODO: Add process code here
    pass
