#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utility.py
@Desc    :   provide utility resources
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/07/12 20:04, MinGo
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
from .api_in import utility_add_par
from .api_in import utility_get_par
from .api_in import utility_put_par
from .api_in import utility_dd_par

# fields
from .api_out import utility_record_fields
from .api_out import utility_records_fields

# app,svc,db processor
from app.mssweb.service import utility as utl_svc
from app.mssweb.dao import utility_processor

# log
import logging
log = logging.getLogger('MSS')

# export
__all__ = [
    'utility',
    'utility_s'
]


# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class utility(Resource):

    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1
    '''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可
    @marshal_with(utility_record_fields)
    def get(self, utility_id):
        #
        obj = utility_processor.fetch(utility_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, utility_id):
        params = utility_put_par.parse_args()
        utility_db_proc = utility_processor(params)
        ret = utility_db_proc.update(unique_keys=["name"])
        return render_data(ret)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, utility_id, session=sss):
        obj = utility_processor.fetch(utility_id, to_user_obj=False)
        session.delete(obj)
        return render_data(utility_id)


class utility_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = utility_add_par.parse_args()
        utility_proc = utility_processor(params)
        rcd = utility_proc.add(unique_keys=["name"])
        return render_data(rcd)

    @marshal_with(utility_records_fields)
    def get(self, category=None, name=''):
        f_params = utility_get_par.parse_args()
        rcds = utl_svc.utility_s_filter(
            f_params, joined_keys=["fk_dict_utility_main_group",
                                   "fk_dict_utility_sub_group"])
        return render_data(rcds)
