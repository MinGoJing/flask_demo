#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session.py
@Desc    :   provide session resource
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/23 06:42, MinGo
          1. Created.

'''

# py

# flask
from flask_restful import Resource
from flask_restful import marshal_with

# app
from app import db

# common
from app.common.db import transaction
from app.common.code import RET
from app.common.http_auth import multi_auth
from app.common.restful_fields import render_data
from app.common.restful_fields import int_record_fields

# parser
from ..api_in import session_add_par
from ..api_in import session_get_par
from ..api_in import session_put_par
from ..api_in import session_dd_par

# fields
from ..api_out import session_record_fields
from ..api_out import session_records_fields

# db processor
from app.msscomp.dao import session_processor

# app
from app.msscomp.app import session_subfeatures_add

# log
import logging
log = logging.getLogger('MSS')

# export
__all__ = [
    'session',
    'session_s'
]


# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class session(Resource):

    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1
    '''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可
    @marshal_with(session_record_fields)
    def get(self, session_id):
        #
        obj = session_processor.fetch(session_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, session_id):
        params = session_put_par.parse_args()
        session_db_proc = session_processor(params)
        ret = session_db_proc.update(unique_keys=[])
        return render_data(ret)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, session_id, session=sss):
        obj = session_processor.fetch(session_id, to_user_obj=False)
        session.delete(obj)
        return render_data(session_id)


class session_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = session_add_par.parse_args()
        session_proc = session_processor(params)
        ss_id = session_proc.add()

        if (params.get("session_inputs") or params.get("session_parameters")):
            session_subfeatures_add(ss_id, params)

        return render_data(ss_id)

    @marshal_with(session_records_fields)
    def get(self, category=None, name=''):
        f_params = session_get_par.parse_args()
        rcds = session_processor.get(f_params)
        return render_data(rcds)
