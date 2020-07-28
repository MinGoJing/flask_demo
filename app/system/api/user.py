#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   user.py
@Desc    :   provide user API
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :
    1.0: 2020/01/12 12:35, MinGo
          1. Created.

'''

# py

# config
from app import conf

# flask
from flask_restful import abort
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# common
from app.common.http_auth import basic_auth
from app.common.http_auth import token_auth

# export
__all__ = [
    "user",
    "user_s"
]

# log
import logging
log = logging.getLogger("SYS")


class user(Resource):

    def user_get(self, user_name):
        return "{}'s main page.".format(user_name)


class user_s(Resource):

    def post(self, ):
        return ""


@token_auth.verify_token
def verify_token(token):
    """
    token认证
        curl -X GET -H "Authorization: Bearer secret-token-1" http://localhost:5000/
    :param token: Bearer secret-token-1
    :return:
    """
    tokens = []

    if (conf.DEBUG):
        return True

    if token in tokens:
        return True

    return False


@token_auth.error_handler
def token_unauthorized():
    """
    认证失败
        flask 需要以return 这种方式返回自定义异常
            return make_response(jsonify({'error': 'Not Find'}), 401)
        flask_restful 则修改abort方式返回自定义异常
            abort(401, message={'error': 'Unauthorized access'})
    :return:
    """
    abort(401, message={'error': 'Unauthorized access'})


@basic_auth.verify_password
def verify_password(username, password):
    """
    用户名密码认证
        curl -u Tom:111111 -i -X GET http://localhost:5000/
    :param username:
    :param password:
    :return:
    """
    # query from sys users
    users = []

    if (conf.DEBUG):
        return True

    for user in users:
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                return True

    return False


@basic_auth.error_handler
def password_unauthorized():
    abort(401, message={'error': 'Unauthorized access'})
