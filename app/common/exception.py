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

# flask
from flask import request, json
from werkzeug.exceptions import HTTPException

# local
from .code import RET

# log
import logging
log = logging.getLogger("MSS")


class APIException(HTTPException):
    """
    base data & code render Exception
    """
    _ret_cls = RET
    # key data 4 msg content
    data = None
    # full environment data
    raw_data = None
    result_code = RET.E_UNEXPECTED
    msg = "Ops, API unexpected error occurs."

    def __init__(self, data=None, msg="", raw_data=None, lan="en"):
        self.data = data
        self.msg = "%s: %s" % (self._ret_cls.INFO(
            self.result_code, lan), self.msg)
        self._init_msg(data, msg)
        self.code = self.status

        log.error(self.msg)
        HTTPException.__init__(self, self.msg)

    def __str__(self):
        return self.msg

    def get_headers(self, environ=None):
        return [("content-type", "application/json")]

    def get_body(self, environ=None):
        resp = {
            "msg": self.msg,
            "code": self.result_code,
            "data": self.raw_data
        }
        return json.dumps(resp)

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
        elif (not msg.startswith(RET.INFO(self.result_code))):
            msg = "%s: %s" % (RET.INFO(self.result_code), msg)
        else:
            self.msg = msg

        return

    @property
    def status(self):
        hex_code = (self.result_code >> 8) & (0x0FFF)
        http_code = (hex_code >> 8) * 100 + \
            ((hex_code >> 4) & 0x0F) * 10 + (hex_code & 0x0F)
        return http_code


class InvalidEntityClsException(APIException):
    """
    @data : str
            entity name
    """

    result_code = RET.E_ORM_ENTITY_NOT_FOUND_ERROR
    msg = "db entity[{}] NOT found."


class QueryJoinRuleLengthNotSupportException(APIException):
    """
    @data : str
        str: local_table.db_key

    """
    result_code = RET.E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR
    msg = ("db entity join <{}> rule length NOT supported.")


class EntityAutoJoinFailedException(APIException):
    """
    @data : str: 
            'local_table.db_key'

    """
    result_code = RET.E_ENTITY_AUTO_JOIN_FAILED
    msg = ("db entity AUTO join from <{}> failed.")


class BadParameterException(APIException):
    """
    @data : (str, type1, any_value, type2)
        @str  : parameter name
        @type1: current type
        @any  : current value
        @type2: required type
    """
    result_code = RET.E_BAD_PARAMETER
    msg = ("parameter[{}<{}> : {}] NOT in required type<{}>")


class InvalidArgsException(APIException):
    """
    @data : str : invalid parameter names seperated with ','
    """
    result_code = RET.E_INVALID_ARG
    msg = ("NOT all parameters[{}] were given.")


class QueryMapFormatException(APIException):
    """
    @data : str : error query map keys seperated with ','
    """
    result_code = RET.E_BAD_PARAMETER
    msg = "entity <{}> query map keys<{}> error."


class StringFieldEmptyException(APIException):
    """
    @data : str
            filed name.
    """
    result_code = RET.E_INVALID_ARG
    msg = ("String field<{}> is empty.")


class EntityUpdateUniqueKeyExistsException(APIException):
    """
    @data : (<str1>, <list:str2>)
        @str1: DB entity table name;
        @str2: unique key item of list;
    """
    result_code = RET.E_ENTITY_UPDATE_UNIQUE_ERROR
    msg = ("Entity <{}> object add/update <{}> unique check error.")


class EntityBackrefAttributeNotFoundException(APIException):
    """
    @data : (str, str)
        @str : entity_tale_name
        @str : entity backref attribute
    """
    result_code = RET.E_ENTITY_BACKREF_NOT_FOUND_ERROR
    msg = ('entity <{}> backref attribute <{}> NOT found.')


class EntityNotFoundException(APIException):
    """
    @data : (str, int)
        @str : tale_name
        @int : entity_id
    """
    result_code = RET.E_ENTITY_NOT_FOUND
    msg = ('Entity <{} id:{}> NOT FOUND, update failed.')


class DeleteEntityNotFoundException(APIException):
    """
    @data : (str, int)
        @str : entity_tale_name
        @int : entity_id
    """
    result_code = RET.S_DELETE_ENTITY_NOT_FOUND
    msg = ('Entity <{} id:{}> NOT FOUND, delete failed.')


class InitProcessorNotFoundException(APIException):
    """
    @data : str
        @str : table name
    """
    result_code = RET.E_INIT_PROCESSOR_TABLENAME_NOT_FOUND
    msg = ('Db init, table<{}> InitProcessor NOT found.')


class DbEntityInitTableDataNotFoundException(APIException):
    """
    @data : str
        @str : table name
    """
    result_code = RET.E_INIT_PROCESSOR_TABLE_DATA_NOT_FOUND
    msg = ('Db init, table<{}> datasheet NOT found.')


class DBEntityRemoteReferenceNotMatchException(APIException):
    """
    @data : str1, str2, str3
        @str1: local table name
        @str2: reference key
        @str3: value
    """
    result_code = RET.E_ENTITY_REFERENCE_KEY_ERROR
    msg = ('Entity<{}> reference key<{}> value<{}>, did NOT found remote entity to match.')
