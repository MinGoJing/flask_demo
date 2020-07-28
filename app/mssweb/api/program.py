#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   program.py
@Desc    :   provide program resources
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/28 23:32, MinGo
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
from .api_in import program_add_par
from .api_in import program_get_par
from .api_in import program_put_par
from .api_in import program_dd_par

# fields
from .api_out import program_record_fields
from .api_out import program_records_fields

# db processor
from app.mssweb.dao import program_processor

# log
import logging
log = logging.getLogger('MSS')

# export
__all__ = [
    'program',
    'program_s'
]


# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class program(Resource):

    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1
    '''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可
    @marshal_with(program_record_fields)
    def get(self, program_id):
        #
        obj = program_processor.fetch(program_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, program_id):
        params = program_put_par.parse_args()
        ret = program_processor.update(program_id, params)
        return render_data(ret)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, program_id, session=sss):
        rcd = program_processor.delete(program_id)
        if (not rcd):
            raise Exception()
            return render_data(rcd)
        return render_data(program_id)


class program_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = program_add_par.parse_args()
        program_proc = program_processor(params)
        rcd = program_proc.add()
        return render_data(rcd)

    @marshal_with(program_records_fields)
    def get(self, category=None, name=''):
        f_params = program_get_par.parse_args()
        rcds = program_processor.get(f_params)
        return render_data(rcds)
