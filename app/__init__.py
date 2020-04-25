#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide app module init process.
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :   
    1.0: 2020/01/11 18:31, MinGo
          1. Created.

'''
# py
from app.mingo.api import user
import sys
from os import path

# flask
from flask import Flask
from werkzeug import import_string

app = Flask(__name__)

# PROJ_HOME_PATH
PROJ_HOME_PATH = path.abspath(
    path.join(path.dirname(path.abspath(__file__)), ".."))
sys.path.insert(0, PROJ_HOME_PATH)

print(sys.path)

# blue prints
blueprints = [
    "app.mingo.api.hello:hello",
    "app.mingo.api.user:user"
]


for bp in blueprints:
    bp_obj = import_string(bp)
    app.register_blueprint(bp_obj)
