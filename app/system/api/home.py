#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   home.py
@Desc    :   provide home api
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/05/18 05:28, MinGo
          1. Created.

'''

# py

# flask
from flask import Blueprint

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "home",
    "home_get"
]


home = Blueprint("home", __name__, url_prefix="/")


@home.route("/", methods=["GET"], endpoint="home_get")
def home_get():
    return "{}'s main page.".format("home")
