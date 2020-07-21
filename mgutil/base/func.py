#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   func.py
@Desc    :   provide basic functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/05/14 05:27, MinGo
          1. Created.

'''

# py
import platform

# local

# export
__all__ = [
    "SLASH",
]


# SLASH
SLASH = None
if (SLASH is None):
    if (platform.system() == "Windows"):
        SLASH = "\\"
    else:
        SLASH = "/"


# def export_sub_model_content(model_folder_path, project_home_path):
#     #
#     model_folder_path = path.abspath(model_folder_path)
#     project_home_path = path.abspath(project_home_path)+SLASH
#     if (not model_folder_path.startswith(project_home_path)):
#         assert(False)

#     import_path = model_folder_path.replace(
#         project_home_path, '').replace(SLASH, '.')

#     #
#     sub_modules = mgf_match_ls_sub_names(model_folder_path,
#                                          match_exp="^(?!_).+$",
#                                          is_path_relative=True, match_opt=0)
#     for mod in sub_modules:
#         mod_name = mod.split('.')[0]
#         import_case = "%s.%s" % (import_path, mod_name)
#         export_list = import_string("%s:__all__" % (import_case))
#         for item in export_list:
#             import_string("%s:%s" % (import_case, item))
