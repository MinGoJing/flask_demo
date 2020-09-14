#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exc.py
@Desc    :   provide exceptions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/08/08 21:37, MinGo
          1. Created.

'''

# py

# local

# log
import logging
log = logging.getLogger('UTIL')


class UtilBaseException(Exception):
    # key data 4 msg content
    data = None
    code = 0
    # full environment data
    raw_data = None
    msg = "Ops, API unexpected error occurs."

    def __init__(self, data=None, msg="", code=0, raw_data=None, lan="en"):
        self.data = data
        self._init_msg(data, msg)
        self.code = code

        log.error(self.msg)
        Exception.__init__(self, self.msg)

    def __str__(self):
        return self.msg

    def _init_msg(self, data=None, msg=""):
        if (data and not msg):
            try:
                if (not isinstance(data, (tuple, list, dict))):
                    self.msg = self.msg.format(data)
                elif (isinstance(data, (list, tuple))):
                    p_cnt = self.msg.count("{}")
                    if (p_cnt == len(data)):
                        self.msg = self.msg.format(*data)
                    elif (p_cnt == 1):
                        self.msg = self.msg.format(data)
                    else:
                        assert(-1)
                elif (isinstance(data, (dict))):
                    self.msg = self.msg.format(**data)
            except Exception as e:
                print(e)
                assert(-1)
        else:
            self.msg = msg

        return


class SubFeatureFilterTypeNotSupportException(UtilBaseException):
    """
    @data : str
        @str : typename
    """
    msg = ('Sub feature filter NOT supported for type<{}>')


class SubFeatureFilterKeyNotFoundException(UtilBaseException):
    """
    @data : (str1, str2)
        @str1 : full key path
        @str2 : not found key
    """
    msg = ('Sub feature filter key <{} :: {}> NOT found error')


class SubFeatureDictIndexKeyNotFoundException(UtilBaseException):
    """
    @data : str
        @str : key name
    """
    msg = ('Sub feature dict source key <{}> NOT found error')


class SubFeatureDictIndexKeyValueRepeatException(UtilBaseException):
    """
    @data : (str1, str2)
        @str1 : key name
        @str2 : key value
    """
    msg = ('Sub feature dict source key <{}> value<{}> repeated')


class SubFeatureDictMultiTargetValueException(UtilBaseException):
    """
    @data : str
        @str : key name
    """
    msg = ('Sub feature dict target key value <{}> more than one')


class SubFeatureMarshalTargetAttributeLostException(UtilBaseException):
    """
    @data : (str, any)
        @str1 : source match key path
        @any : source match key value
    """
    msg = ('Sub feature marshal source key<{}> value<{}>, lost target attribute')


class XlsxWriteNotSupportedException(UtilBaseException):
    """
    @data : str
        @str : filepath
    """
    msg = ('Xlsx File<{}> Write NOT supported yet')


class FileRemovePermissionDeniedException(UtilBaseException):
    """
    @data : (str1, str2)
        @str1 : file path
        @str2 : exception string
    """
    msg = ('File<{}> remove failed: {}')


class FolderCreateException(UtilBaseException):
    """
    @data : str
        @str : Create folder path
    """
    msg = ('Folder<{}> create failed.')


class Str2CodecException(UtilBaseException):
    """
    @data : str1, str2
        @str1 : str
        @str2 : codec str
    """
    msg = ('String<{}> to codec<{}> failed.')
