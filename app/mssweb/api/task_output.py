#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   task_output.py
@Desc    :   provide task output resources
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/07/31 06:14, MinGo
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
from .api_in import task_output_add_par
from .api_in import task_output_get_par
from .api_in import task_output_put_par
from .api_in import task_output_dd_par

# fields
from .api_out import task_output_record_fields
from .api_out import task_output_records_fields

# db processor
from app.mssweb.dao import task_output_processor

# log
import logging
log = logging.getLogger('MSS')

# export
__all__ = [
    'task_output',
    'task_output_s'
]


# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class task_output(Resource):

    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1
    '''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可
    @marshal_with(task_output_record_fields)
    def get(self, task_output_id):
        #
        obj = task_output_processor.fetch(task_output_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, task_output_id):
        params = task_output_put_par.parse_args()
        rcd = task_output_processor.update(task_output_id, params)
        return render_data(rcd)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, task_output_id, session=sss):
        task_output_processor.delete(task_output_id)
        return render_data(task_output_id)


class task_output_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = task_output_add_par.parse_args()
        task_output_proc = task_output_processor(params)
        rcd = task_output_proc.add()
        return render_data(rcd)

    @marshal_with(task_output_records_fields)
    def get(self, category=None, name=''):
        f_params = task_output_get_par.parse_args()
        rcds = task_output_processor.get(f_params)
        return render_data(rcds)
