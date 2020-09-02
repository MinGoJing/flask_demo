#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   xls_test.py
@Desc    :   provide xls parser test cases
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/09/02 05:28, MinGo
          1. Created.

'''

# py
import os

# util
from mgutil.parser import xls_std_parse
from mgutil.parser import xls_std_dump


def test_main():
    msg = "ok"
    from app import PROJ_HOME_PATH

    #
    in_file_path = os.path.join(PROJ_HOME_PATH, "test/xls_parser/case01.xls")
    xls_sheet, msg = xls_std_parse(in_file_path)
    for sheet_name, data_sheet in xls_sheet.items():
        print("Sheet<%s>:" % (sheet_name))
        print("%s\n" % (data_sheet))

    out_file_path = in_file_path.replace("case01", "case01_dump")
    bret = xls_std_dump(out_file_path, xls_sheet)

    print("done.")
    return True, msg


if ("__main__" == __name__):
    test_main()
