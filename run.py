#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   run.py
@Desc    :   provide app running entrance
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :   
    1.0: 2020/01/12 11:52, MinGo
          1. Created.

'''

# py

# app
from app import app

if ("__main__" == __name__):
    app.run("127.0.0.1", port=8080)
