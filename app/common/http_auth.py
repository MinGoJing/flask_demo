#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   http_auth.py
@Desc    :   provide http auth
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/05/26 06:37, MinGo
          1. Created.

'''

# py

# flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

# export
__all__ = [
    "basic_auth",
    "token_auth",
    "multi_auth"
]


# 用户名密码方式认证
basic_auth = HTTPBasicAuth()
# 令牌（Token）认证
token_auth = HTTPTokenAuth(scheme='Bearer')
# 以上两种多重认证-若期中之一通过，则认证通过
multi_auth = MultiAuth(basic_auth, token_auth)
