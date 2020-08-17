#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   string.py
@Desc    :   provide string functions
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :   
    1.0: 2020/08/17 21:06, MinGo
          1. Created.

'''

# py


from chardet import UniversalDetector

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


def str2codec(src_str, codec):
    # args
    if (not is_string(src_str)):
        return False, src_str
    if (0 == len(src_str)):
        return True, src_str

    # locals
    str_codec = ""
    # unicode, encode direct
    if (type(u"") == type(src_str)):
        src_str = src_str.encode(codec)
        return True, src_str

    # init
    u = UniversalDetector()
    u.feed(src_str)
    u.close()
    codec_obj = u.result
    str_codec = codec_obj["encoding"]
    # equal
    if (str_codec == codec):
        return True, src_str

    # try codec
    try:
        if ("Windows-1252" == str_codec or str_codec.starswith("ISO-8859-1")):
            pass
            # str_str = src_str.replace("，", ",")
        else:
            str_str = src_str.decode(str_codec).encode(codec)
    except Exception as e:
        log.error(str(e))
        return False, str_str
    return True, str_str
