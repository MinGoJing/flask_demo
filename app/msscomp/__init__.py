#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide msscomp resources
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/22 06:22, MinGo
          1. Created.

'''

# py

# api error
from .api.error import errors
# api resource
from .api.resource.session import session
from .api.resource.session import session_s
from .api.resource.session_output import session_output
from .api.resource.session_output import session_output_s
from .api.resource.session_output_value import session_output_value
from .api.resource.session_output_value import session_output_value_s


def init_module(api):
    # merge exceptions
    # api.errors.update(errors)

    # add resource
    api.add_resource(session, '/session/<session_id>', endpoint='session')
    api.add_resource(session_s, '/sessions', endpoint='sessions')
    api.add_resource(
        session_output, '/session_output/<session_output_id>', endpoint='session_output')
    api.add_resource(session_output_s, '/session_outputs',
                     endpoint='session_outputs')
    api.add_resource(session_output_value,
                     '/session_output_value/<session_output_value_id>', endpoint='session_output_value')
    api.add_resource(session_output_value_s,
                     '/session_output_values', endpoint='session_output_values')
