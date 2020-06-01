#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   file.py
@Desc    :   provide file & directory handle functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/25 22:10, MinGo
          1. Created.

'''

# py
import shutil
import os
import re
import logging


# globals
log = logging.getLogger("SYS")


# Desc  : get ls results matches “match_exp” in directory [tar_dir]
# Input   -
#   1. (str)tar_dir: target directory
#   2. (str)match_exp: match expression
#   3. (E_FILE_PATH_MODE):
#     a. E_FILE_PATH_MODE.ABSOLUTE(0)
#     b. E_FILE_PATH_MODE.RELATIVE(1)
#   4. (int)match_opt: match config
#     a. 0: match file and directory
#     b. 1: match directory only
#     c. 2: match file only
#   5. (int)uniq: same value appears once
# Return  -
#   1. (list[str]): ls results
def mgf_match_ls_sub_names(tar_dir, match_exp=None, is_path_relative=True,
                           match_opt=0):
    from app import conf

    if (not os.path.isdir(tar_dir)):
        log.error("["+tar_dir+"] is NOT a directory.")
        return []

    contends = os.listdir(tar_dir)

    retNameList = []
    if (0 == match_opt):
        if (match_exp is not None):
            for item in contends:
                if (re.match(match_exp, item) is not None):
                    retNameList.append(item)
        else:
            retNameList = contends
    elif (1 == match_opt):
        if (match_exp is not None):
            for item in contends:
                if (os.path.isdir(tar_dir+conf.SLASH+item)):
                    if (re.match(match_exp, item) is not None):
                        retNameList.append(item)
        else:
            for item in contends:
                if (os.path.isdir(tar_dir+conf.SLASH+item)):
                    retNameList.append(item)

    elif (2 == match_opt):
        if (match_exp is not None):
            for item in contends:
                if (os.path.isfile(tar_dir+conf.SLASH+item)):
                    if (re.match(match_exp, item) is not None):
                        retNameList.append(item)
        else:
            for item in contends:
                if (os.path.isfile(tar_dir+conf.SLASH+item)):
                    retNameList.append(item)

    if (not is_path_relative):
        # prepare
        mPreCwd = os.getcwd()
        os.chdir(tar_dir)
        for i in range(0, len(retNameList)):
            retNameList[i] = os.path.abspath(retNameList[i])
        os.chdir(mPreCwd)

    return retNameList
