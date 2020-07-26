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
from ..dao import session_input_value_processor
from ..dao import session_parameter_processor
from ..dao import session_parameter_value_processor


def session_subfeatures_add(ss_id, params):
    #
    ss_inputs = params.get("session_inputs")
    ss_parameters = params.get("session_parameters")

    # add inputs
    input_procs = [session_input_processor(obj) for obj in ss_inputs]
    for obj in input_procs:
        obj.session_id = ss_id
        input_id = session_input_processor.add(obj)

        # add input values
        if (obj.input_values):
            iv_procs = [session_input_value_processor(
                iv) for iv in obj.input_values]
            for iv_obj in iv_procs:
                iv_obj.session_input_id = input_id
            iv_rcd = session_input_value_processor.add_many(iv_procs)

    # add parameters
    parameter_procs = [session_parameter_processor(
        obj) for obj in ss_parameters]
    for obj in parameter_procs:
        obj.session_id = ss_id
        parameter_id = session_parameter_processor.add(obj)

        # add parameter values
        if (obj.parameter_values):
            pv_procs = [session_parameter_value_processor(
                iv) for iv in obj.parameter_values]
            for iv_obj in pv_procs:
                iv_obj.session_parameter_id = parameter_id
            pv_rcd = session_parameter_value_processor.add_many(pv_procs)

    return len(input_procs), len(parameter_procs)
