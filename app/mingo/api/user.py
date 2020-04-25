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

# flask
from flask import Blueprint, render_template

# export
__all__ = [
    "user"
]

# log
import logging
log = logging.getLogger("SYS")

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/<user_name>", methods=["GET"], endpoint="user_get")
def user_get(user_name):
    return "{}'s main page.".format(user_name)
