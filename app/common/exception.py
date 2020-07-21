#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   exception.py
@Desc    :   provide common exceptions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/18 21:48, MinGo
          1. Created.

'''

# py

# local
from .code import RET

# log
import logging
log = logging.getLogger("MSS")


class BaseDataRenderException(Exception):
    """
    base data & code render Exception
    """
    _data = None
    _code = None

    def __init__(self, msg="Data Render Message", code: int = RET.S_OK, data=None):
        self._data = data
        self._code = code
        Exception.__init__(self, msg)

    @property
    def code(self):
        return self._code

    @property
    def data(self):
        return self._data

    @property
    def http_code(self):
        hex_code = (self._code >> 8) & (0x0FFF)
        http_code = (hex_code >> 8) * 100 + \
                    ((hex_code >> 4) & 0x0F) * 10 + (hex_code & 0x0F)
        return http_code


class InvalidEntityClsException(BaseDataRenderException):
    """
    @data : str
            Entity class name.
    """

    def __init__(self, data, msg=""):
        code = RET.E_ORM_ENTITY_NOT_FOUND_ERROR
        if (not msg):
            msg = "%s: db entity[%s] NOT found." % (RET.INFO(code), data)
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(self, msg, code, data=data)


class QueryJoinRuleLengthNotSupportException(BaseDataRenderException):
    """
    @data : str
        str: local_table.db_key

    """

    def __init__(self, data, msg=""):
        code = RET.E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR
        if (not msg):
            msg = ("%s: db entity join from %s rule length NOT supported." % (
                RET.INFO(code), data))
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        BaseDataRenderException.__init__(self, msg, code, data=data)


class EntityAutoJoinFailedException(BaseDataRenderException):
    """
    @data : str 'local_table.db_key'

    """

    def __init__(self, data, msg=""):
        code = RET.E_ENTITY_AUTO_JOIN_FAILED
        if (not msg):
            msg = ("%s: db entity AUTO join from %s failed." % (
                RET.INFO(code), data))
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(self, msg, code, data=data)


class BadParameterException(BaseDataRenderException):
    """
    @data :
        {
            "name": <str>,
            "value": <Any>,
            "type_req": <type>  # type required
        }
    """

    def __init__(self, data: dict, msg=""):
        code = RET.E_BAD_PARAMETER
        if (not msg):
            msg = ("%s: parameter[%s<%s> : %s] NOT in required type<%s>"
                   % (RET.INFO(code), data.get("name"), type(data.get("value")),
                      data.get("value"), data.get("type_req")))
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(
            self, msg, code, data=data)


class InvalidArgsException(BaseDataRenderException):
    """
    @data :
        [
            {
                "name": <str>,
                "type": <type>
            },
            ...
        ]
    """

    def __init__(self, data: list, msg=""):
        code = RET.E_BAD_PARAMETER
        if (not msg):
            args = ""
            if ((isinstance(data, list)
                 or isinstance(data, tuple))
                    and data):
                args = "%s<%s>" % (data[0].get("name"), data[0].get("type"))
                if (1 < len(data)):
                    for i in range(1, len(data)):
                        d = data[i]
                        args = "%s, %s<%s>" % (
                            args, d.get("name"), d.get("type"))

            msg = ("%s: NOT all parameters[%s] were given." % (
                RET.INFO(code), args))
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(
            self, msg, code, data=data)


class QueryMapFormatException(BaseDataRenderException):
    """

    """

    def __init__(self, data: dict, msg=""):
        code = RET.E_BAD_PARAMETER
        if (not msg):
            msg = "%s: %s" % (RET.INFO(code), msg)
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(
            self, msg, code, data=data)


class StringFieldEmptyException(BaseDataRenderException):
    """
    @data : str
            filed name.
    """

    def __init__(self, data: str, msg=""):
        code = RET.E_INVALID_ARG
        if (not msg):
            msg = "{}: String field<{}> is empty.".format(RET.INFO(code), data)
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(self, msg, code, data)


class EntityUpdateUniqueKeyExistsException(BaseDataRenderException):
    """
    @data : (<str1>, <list:str2>). if msg is EMPTYs
                str1: DB entity table name;
                str2: unique key item of list;
            <int>. if msg is NOT EMPTY
                int: process result, usually
    """

    def __init__(self, data, msg=""):
        code = RET.E_ENTITY_UPDATE_UNIQUE_ERROR
        if (not msg):
            if (isinstance(data, (list, tuple))):
                msg = ("{}: Entity <{}> object add/update <{}> unique check error.".format(
                    RET.INFO(code), *data))
            else:
                msg = ("{}: Entity object add/update failed 4 unique key check error.".format(
                    RET.INFO(code)))
        elif (not msg.startswith(RET.INFO(code))):
            msg = "%s: %s" % (RET.INFO(code), msg)

        log.error(msg)
        BaseDataRenderException.__init__(self, msg, code, data=0)
