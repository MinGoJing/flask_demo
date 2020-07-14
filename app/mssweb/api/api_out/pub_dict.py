#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pub_dict_field.py
@Desc    :   provide pub dict local field definitions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/28 06:53, MinGo
          1. Created.

'''

# py

# flask
from flask_restful import fields

# export
__all__ = [
    "pub_dict_record_field",
    "pub_dict_record_fields",
    "pub_dict_records_fields"
]


# local fields
#
pub_dict_record_field = {
    "id": fields.Integer(attribute="id2"),
    "name": fields.String,
    "disabled": fields.Boolean,
    "category": fields.String,
    "operator_id": fields.Integer,
    "operator_name": fields.String,
    "operate_time": fields.DateTime(),
    "note": fields.String,
}


# API fields
#
pub_dict_record_fields = {
    "msg": fields.String(default="ok"),
    "code": fields.Integer,
    "data": fields.Nested(pub_dict_record_field),
}

pub_dict_records_fields = {
    "msg": fields.String(default="ok"),
    "code": fields.Integer,
    "data": fields.List(fields.Nested(pub_dict_record_field)),
}
