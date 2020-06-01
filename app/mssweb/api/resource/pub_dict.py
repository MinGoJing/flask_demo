#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pub_dict.py
@Desc    :   provide pub dict APIs
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/22 00:08, MinGo
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
from app.common.http_auth import multi_auth
from app.common.restful_fields import render_data
from app.common.restful_fields import int_record_fields

# parser
from ..parser import dict_add_par
from ..parser import dict_get_par
from ..parser import dict_put_par
from ..parser import dict_dd_par

# fields
from ..field import pub_dict_record_fields
from ..field import pub_dict_records_fields

# db processor
from app.mssweb.dao import pub_dict_processor, PubDict

# export
__all__ = [
    "pub_dict",
    "pub_dict_s",
]

# log
import logging
log = logging.getLogger("SYS")

# global, do NOT let db.session to generate many scoped_sessions
sss = db.session


class pub_dict(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]
    '''
    若采用flask注解方式认证，在对应方法上添加下列装饰器，3选1'''
    # @basic_auth.login_required  # 用户名密码认证方式
    # @token_auth.login_required  # token认证方式
    # @multi_auth.login_required  # 两种综合认证方式，满足其一即可

    @marshal_with(pub_dict_record_fields)
    def get(self, dict_id):
        #
        obj = pub_dict_processor.fetch(dict_id)
        return render_data(obj)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def put(self, dict_id):
        params = dict_put_par.parse_args()
        dict_db_proc = pub_dict_processor(params)
        ret = dict_db_proc.update()
        return render_data(ret)

    @marshal_with(int_record_fields)
    @transaction(session=sss)
    def delete(self, dict_id, session=sss):
        obj = pub_dict_processor.fetch(dict_id, to_user_obj=False)
        session.delete(obj)
        return render_data(dict_id)


class pub_dict_s(Resource):
    # flask_restful 安全认证方式，类似于flask注解，全局认证
    # decorators = [multi_auth.login_required]

    @marshal_with(int_record_fields)
    def post(self):
        params = dict_add_par.parse_args()
        pub_dict_proc = pub_dict_processor(params)
        dict_id = pub_dict_proc.add()
        return render_data(dict_id)

    @marshal_with(pub_dict_records_fields)
    def get(self, category=None, name=""):
        f_params = dict_get_par.parse_args()
        rcds = pub_dict_processor.get(f_params)
        return render_data(rcds)
