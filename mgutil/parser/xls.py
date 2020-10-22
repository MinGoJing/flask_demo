#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   xls.py
@Desc    :   provide excel parser and utils
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/08/13 22:24, MinGo
          1. Created.

'''

# py
import os
from os import path
import xlrd
import xlwt

# local
from . file import file_basename_first_part
from .. base.string import str2codec
from .. base.exc import XlsxWriteNotSupportedException
from .. base.exc import FolderCreateException
from .. base.exc import FileRemovePermissionDeniedException
from .. base.exc import Str2CodecException


# log
import logging
log = logging.getLogger('UTIL')

# export
__all__ = [
    "xls_std_parse",
    "xls_std_dump"
]


def _xls_obj_parse(file_path):
    if (not path.exists(file_path)):
        return None

    #
    xls_obj = None
    try:
        xls_obj = xlrd.open_workbook(file_path)
    except Exception as e:
        e = e

    return xls_obj


def xls_std_parse(file_path, b_skip_empty_rol=False):
    msg = "ok"
    sheet_dict = {}

    xls_obj = _xls_obj_parse(file_path)
    if (not xls_obj):
        msg = "No data found in file<{}>".format(file_path)
        return sheet_dict, msg

    tabs = xls_obj.sheets()

    for tab in tabs:
        tab_name = tab.name
        if (tab_name.startswith("Sheet") and (1 < len(tabs))):
            tab_name = file_basename_first_part(file_path)
        # if name exists, append records
        dt_list = sheet_dict.get(tab.name, [])

        nrows = tab.nrows
        ncols = tab.ncols
        if (not nrows):
            sheet_dict[tab_name] = dt_list
            continue

        col_name_list = tab.row_values(0)
        for x in range(1, nrows):
            row = tab.row_values(x)
            if row:
                app = {}
                for y in range(0, ncols):
                    ctype = tab.cell(x, y).ctype
                    if (3 != ctype):
                        app[col_name_list[y]] = row[y] if (
                            str(row[y])) else None
                    else:
                        app[col_name_list[y]] = xldate.xldate_as_datetime(
                            row[y], 0)
                if (b_skip_empty_rol and not ("".join(map(lambda x: str(x), app.values())))):
                    # skip empty rol
                    continue

                dt_list.append(app)
        sheet_dict[tab_name] = dt_list

    return sheet_dict, msg


def xls_std_dump(o_file_path, data_sheets={}, b_force=False):
    #
    if (o_file_path.endswith(".xlsx")):
        raise XlsxWriteNotSupportedException(o_file_path)

    #
    if (b_force and os.path.exists(o_file_path)):
        try:
            os.remove(o_file_path)
        except Exception as e:
            log.error(str(e))
            raise FileRemovePermissionDeniedException(o_file_path)

    #
    folder_path = path.dirname(path.abspath(o_file_path))
    if (not path.exists(folder_path)):
        # create folder
        try:
            os.makedirs(folder_path)
        except Exception as e:
            e = e
            raise FolderCreateException(folder_path)

    try:
        workbook = xlwt.Workbook()
        for sheet_name, data_list in data_sheets.items():
            worksheet = workbook.add_sheet(sheet_name)
            col_names = []
            if (data_list):
                col_names = [key for key in data_list[0]]

            # write column features
            row_idx = 0
            for col_idx in range(len(col_names)):
                worksheet.write(row_idx, col_idx, col_names[col_idx])
            row_idx += 1

            # write data lines
            for data in data_list:
                for col_idx in range(len(col_names)):
                    col_name = col_names[col_idx]
                    v = data.get(col_name)
                    # parse float(*.0) to int
                    if (isinstance(v, float) and str(v).endswith(".0")):
                        v = int(v)
                    elif (isinstance(v, str)):
                        bret, v = str2codec(v, encoding="utf-8")
                        if (not bret):
                            raise Str2CodecException(v, "utf-8")
                    worksheet.write(row_idx, col_idx, v)
                row_idx += 1

        workbook.save(o_file_path)
    except Exception as e:
        log.error(str(e))
        return False

    return True


if ("__main__" == __name__):
    from app import PROJ_HOME_PATH
    import sys

    sys.path.insert(0, PROJ_HOME_PATH)

    #
    in_file_path = os.path.join(PROJ_HOME_PATH, "test/xls_parser/case01.xls")
    xls_sheet, msg = xls_std_parse(in_file_path)
    for sheet_name, data_sheet in xls_sheet.items():
        print("Sheet<%s>:\n" % (sheet_name))
        print("%s" % (data_sheet))

    out_file_path = in_file_path.replace("case01", "case01_dump")
    bret = xls_std_dump(out_file_path, xls_sheet)

    print("done.")
