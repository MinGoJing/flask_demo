#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Desc    :   provide app module init process.
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, mingjun_jing
@History :
    1.0: 2020/01/11 18:31, MinGo
          1. Created.

'''
# py
import os
import sys
import shutil
import logging
import logging.config
import platform
from os import path

# flask
from flask import Flask
from werkzeug import import_string
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# util
from mgutil.db import Mysql
from mgutil.parser import mgt_c_yaml_object
from mgutil.file import mgf_match_ls_sub_names


# init PROJ_HOME_PATH & basic PYTHONPATH
#
PROJ_HOME_PATH = path.abspath(
    path.join(path.dirname(path.abspath(__file__)), ".."))
sys.path.insert(0, PROJ_HOME_PATH)
# init log dir
log_path = path.join(PROJ_HOME_PATH, "log")
if (not path.exists(log_path)):
    os.mkdir(log_path)

# parse configs
#
# db & log config
config_path = path.join(PROJ_HOME_PATH, "config.yml")
conf = mgt_c_yaml_object(config_path)
# scheduler config
schedule_cfg_path = path.join(PROJ_HOME_PATH, "config_schedule.yml")
schedule_conf = mgt_c_yaml_object(schedule_cfg_path)


# init system SLASH
#
if (platform.system() == "Windows"):
    setattr(conf, "SLASH", "\\")
else:
    setattr(conf, "SLASH", "/")

# trd part source code debug using
if (conf.DEBUG):
    TRD_HOME = PROJ_HOME_PATH + conf.SLASH + "trd"
    TRD_SOURCES = mgf_match_ls_sub_names(TRD_HOME,
                                         match_exp="^[^_]+$",
                                         is_path_relative=True, match_opt=1)
    for name in TRD_SOURCES:
        trd_path_home = TRD_HOME + conf.SLASH + name
        sys.path.insert(1, trd_path_home)
        print("Add source env: {}".format(name))

# init flask app
#
app = Flask(__name__)

# init app secret key
#
app.secret_key = os.urandom(32)

# init from yml conf
#
# init logger
logging.config.dictConfig(conf.LOGGER.to_json())
log = logging.getLogger("SYS")
# init db
db_debug_prefix = ""
if (conf.DEBUG):
    db_debug_prefix = "DEBUG_"
db_conf = conf.DB.MYSQL.to_json({"%sHOST" % (db_debug_prefix): "host",
                                 "%sPORT" % (db_debug_prefix): "port",
                                 "%sDB" % (db_debug_prefix): "db",
                                 "%sUSER" % (db_debug_prefix): "user",
                                 "%sPASSWORD" % (db_debug_prefix): "password",
                                 "SQLALCHEMY_DATABASE_URI": "SQLALCHEMY_DATABASE_URI",
                                 "DEBUG_SQLALCHEMY_DATABASE_URI": "DEBUG_SQLALCHEMY_DATABASE_URI",
                                 "SQLALCHEMY_TRACK_MODIFICATIONS": "SQLALCHEMY_TRACK_MODIFICATIONS",
                                 "SQLALCHEMY_ECHO": "SQLALCHEMY_ECHO"})
db = None
if (conf.DB.USE_SQLALCHEMY):
    # init sqlalchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = db_conf["%sSQLALCHEMY_DATABASE_URI" % (
        db_debug_prefix)]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = db_conf["SQLALCHEMY_TRACK_MODIFICATIONS"]
    app.config["SQLALCHEMY_ECHO"] = db_conf["SQLALCHEMY_ECHO"]
    db = SQLAlchemy(app, session_options={'autocommit': True})
    db_conf.pop("SQLALCHEMY_DATABASE_URI")
    db_conf.pop("SQLALCHEMY_TRACK_MODIFICATIONS")
    dbc = Mysql(**db_conf)
else:
    # init db Mysql Client
    dbc = Mysql(**db_conf)


# APIs & Resource init
#
# api
sub_modules = mgf_match_ls_sub_names(PROJ_HOME_PATH + conf.SLASH + "app",
                                     match_exp="^[^_]+$",  # (?!msscomp)
                                     is_path_relative=True, match_opt=1)
api = Api(app)
# register blue prints
for mod in sub_modules:
    init_module = import_string("app.%s:init_module" % (mod))
    init_module(api)
