#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   string.py
@Desc    :   provide string functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :   
    1.0: 2020/08/17 21:06, MinGo
          1. Created.

'''

# py
import chardet

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "is_string",
    "str2codec"
]


def is_string(obj):
    try:
        obj.lower() + obj.title() + ''
    except Exception as e:
        e = e
        return False
    else:
        return True


def str2codec(src_str, encoding=None):
    # args
    if (not is_string(src_str) and not isinstance(src_str, bytes)):
        return False, src_str
    if (0 == len(src_str)):
        if (encoding is None):
            # empty str is different to empty bytes (b'')
            return True, ""
        return True, src_str

    # locals
    str_codec = ""
    # unicode, encode direct, py3
    if (isinstance(src_str, str)):
        if (encoding is None):
            return True, src_str
        return True, src_str.encode(encoding)

    # init
    codec = chardet.detect(src_str)
    str_codec = codec["encoding"]
    # equal encoding
    if (str_codec == encoding):
        return True, src_str
    elif (encoding is None):
        return True, src_str.decode(str_codec)

    # try codec
    str_str = src_str
    try:
        if (isinstance(src_str, bytes)):
            str_str = src_str.decode(str_codec).encode(encoding)
        elif ("Windows-1252" == str_codec or str_codec.starswith("ISO-8859-1")):
            # why do this, we found problem while doing codec transfer in py2
            str_str = src_str
            pass
        else:
            str_str = src_str.decode(str_codec).encode(encoding)
    except Exception as e:
        log.error(str(e))
        return False, src_str
    return True, str_str


if ("__main__" == __name__):
    byte_str = b'universal'
    uni_str = u"unicode"

    str_utf8 = str2codec(byte_str, "utf-8")
    str_utf8_2 = str2codec(uni_str, "utf-8")
