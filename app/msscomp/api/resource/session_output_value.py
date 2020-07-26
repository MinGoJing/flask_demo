#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   session_output_value.py
@Desc    :   provide session output value
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/24 06:11, MinGo
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
from ..api_in import session_output_value_add_par
from ..api_in import session_output_value_get_par
from ..api_in import session_output_value_put_par
from ..api_in import session_output_value_dd_par

# fields
from ..api_out import session_output_value_record_fields
from ..api_out import session_output_value_records_fields

# db processor
from app.msscomp.dao import session_output_value_processor

# log
import logging
log = logging.getLogger('MSS')

# export
__all__ = [
    'session_output_value',
    'session_output_value_s'
]


# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class session_output_value(Resource):

    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1
    '''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可
    @marshal_with(session_output_value_record_fields)
    def get(self, session_output_value_id):
        #
        obj = session_output_value_processor.fetch(
            session_output_value_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, session_output_value_id):
        params = session_output_value_put_par.parse_args()
        session_output_value_db_proc = session_output_value_processor(
            params)
        ret = session_output_value_db_proc.update(
            unique_keys=["session_output_id", "index"])
        return render_data(ret)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, session_output_value_id, session=sss):
        obj = session_output_value_processor.fetch(
            session_output_value_id, to_user_obj=False)
        session.delete(obj)
        return render_data(session_output_value_id)


class session_output_value_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = session_output_value_add_par.parse_args()
        session_output_value_proc = session_output_value_processor(
            params)
        rcd = session_output_value_proc.add(
            unique_keys=["session_output_id", "index"])
        return render_data(rcd)

    @marshal_with(session_output_value_records_fields)
    def get(self, category=None, name=''):
        f_params = session_output_value_get_par.parse_args()
        rcds = session_output_value_processor.get(f_params)
        return render_data(rcds)
