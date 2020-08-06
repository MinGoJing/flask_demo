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


# api resource
from .api.session import session
from .api.session import session_s
from .api.session_output import session_output
from .api.session_output import session_output_s


def init_module(api):
    # add resource
    api.add_resource(session, '/session/<instance_id>', endpoint='session')
    api.add_resource(session_s, '/sessions', endpoint='sessions')
    api.add_resource(
        session_output, '/session_output/<session_output_key>', endpoint='session_output')
    api.add_resource(session_output_s, '/session_outputs',
                     endpoint='session_outputs')
