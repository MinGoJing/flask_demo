#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   slash.py
@Desc    :   provide slash definition
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/08/21 00:15, MinGo
          1. Created.

'''

# py
import platform

__all__ = [
    "SLASH"
]

SLASH = "/"
if (platform.system() == "Windows"):
    SLASH = "\\"
