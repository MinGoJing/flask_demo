#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   hello.py
@Desc    :   provide hello API
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :   
    1.0: 2020/01/12 12:32, MinGo
          1. Created.

'''
# py

# flask
from flask import Blueprint, render_template

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "hello",
    "hello_get"
]

hello = Blueprint("hello", __name__, url_prefix="/hello")


@hello.route('/<name>', methods=["GET"])
def hello_get(name=None):
    return render_template('hello.html', name=name)
