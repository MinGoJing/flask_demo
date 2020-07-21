#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db.py
@Desc    :   provide db processser
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/15 05:28, MinGo
          1. Created.

'''

# py
import copy
from typing import List
from datetime import datetime
from werkzeug import import_string

# flask
from flask_restful import fields
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import joinedload

# base util
from mgutil.base import mgt_c_object
from mgutil.base import g_exclude_attrs_from_db_model
from mgutil.base import attr_list
from mgutil.deco import transaction

# app
from app import db

# mgutil
from mgutil.file import mgf_match_ls_sub_names

# local
from .code import RET
from .code import FAILED
from .exception import QueryMapFormatException
from .exception import QueryJoinRuleLengthNotSupportException
from .exception import EntityUpdateUniqueKeyExistsException
from .exception import EntityAutoJoinFailedException

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "base_db_model",
    "base_db_update_model",
    "init_db_processors"
]

# global
g_entity_table_2_processor_map = {}


class base_db_model(mgt_c_object):
    """
    @Summary: basic ORM entity processor.
            inherit this, and save a lot time in handlering basic AUDS process.

    @_entity_cls: DB entity Class name.
    @_key_2_db_attr_map: dict from key to attribute.
            key is the API feature name;
            attribute is Class member.
    """
    _exclude_attr_list = None
    _entity_cls = None
    _key_2_db_attr_map = None
    _db_attr_2_key_map = None
    _null_supported_filter_attrs = None

    def __init__(self, in_obj={}, b_reverse=False, entity_cls_name=None, key2attr_map: dict = {}):
        from .exception import InvalidEntityClsException

        if (entity_cls_name):
            Cls = globals().get(entity_cls_name)
            if (not Cls):
                raise InvalidEntityClsException(entity_cls_name)
            else:
                self._entity_cls = Cls
        if (not self._entity_cls):
            raise InvalidEntityClsException(str(entity_cls_name))

        if (self._exclude_attr_list is None):
            self._exclude_attr_list = []
        self._exclude_attr_list += g_exclude_attrs_from_db_model
        if (self._support_attr_list is None):
            self._support_attr_list = []
        self._support_attr_list += set(attr_list(
            self._entity_cls, exclude_attrs=self._exclude_attr_list,
            attr2key_map=self.__class__.db_attr_2_key_map()))
        if (self._default_value_map is None):
            self._default_value_map = {}
        if (self._null_supported_filter_attrs is None):
            self._null_supported_filter_attrs = []

        self._dispatch_relation_attr_default_value()

        if (not isinstance(self._key_2_db_attr_map, dict)):
            self._key_2_db_attr_map = {}
        if (isinstance(key2attr_map, dict)):
            self._key_2_db_attr_map.update(key2attr_map)
        if (self._key_2_db_attr_map and not self._db_attr_2_key_map):
            self._db_attr_2_key_map = copy.deepcopy(
                self.__class__.db_attr_2_key_map())

        mgt_c_object.__init__(self, in_obj, b_reverse)

    def _dispatch_relation_attr_default_value(self):
        # analyze Cls
        Cls = self._entity_cls
        self_relations = inspect(Cls).relationships
        rel_directions = {key: str(v.direction).split("')")[0].split("('")[1]
                          for key, v in self_relations.items()}

        for attr in rel_directions:
            if not (attr in self._default_value_map):
                # slution map attr default from ORM
                self._default_value_map[attr] = loc_analyze_attr_default_value(
                    rel_directions[attr])

    @property
    def null_supported_filter_attrs(self):
        if (not self._null_supported_filter_attrs):
            return []
        return self._null_supported_filter_attrs

    @classmethod
    def ex_join_rules(cls):
        if (hasattr(cls, "_ex_join_rules_from_db_key")):
            return cls._ex_join_rules_from_db_key

        return {}

    @property
    def key_2_db_attr_map(self):
        return self._key_2_db_attr_map

    @classmethod
    def db_attr_2_key_map(cls):
        if (cls._db_attr_2_key_map):
            return cls._db_attr_2_key_map
        if (not cls._key_2_db_attr_map):
            return {}
        else:
            cls._db_attr_2_key_map = {
                value: key for key, value in cls._key_2_db_attr_map.items()}
            return cls._db_attr_2_key_map

    @transaction(session=db.session)
    def add(self, session=db.session, unique_keys=[]):
        if (unique_keys):
            fetch_params = {}
            for key in unique_keys:
                fetch_params[key] = self.__dict__.get(key)
            fetch_obj = self.__class__.fetch(fetch_params)
            if (fetch_obj):
                unique_identifier = ""
                for i in range(0, len(unique_keys)):
                    unique_identifier = "%s, %s:%s" % (
                        unique_identifier, unique_keys[i], self.__dict__.get(unique_keys[i]))
                unique_identifier = unique_identifier[2:]
                msg = ("Entity <{}> obj add unique <{}> check failed.".format(
                    self._entity_cls.__tablename__, unique_identifier))
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=0, msg=msg)
        etty_obj = self.to_model(
            self._entity_cls, attr_map=self._key_2_db_attr_map)
        session.add(etty_obj)
        session.flush()
        return etty_obj.id

    @classmethod
    @transaction(session=db.session)
    def add_many(cls, base_model_obj_list, unique_keys=[], session=db.session):
        if (unique_keys):
            fetch_params = {}
            unique_identifier = ""
            obj0 = base_model_obj_list[0]
            if (1 == len(unique_keys)):
                key = unique_keys[0]
                fetch_params[key] = {"op": "in",
                                     "value": [obj.__dict__.get(key) for obj in base_model_obj_list]}
                fetch_objs = obj0.__class__.get(fetch_params)
                if (fetch_objs):
                    for fetch_obj in fetch_objs:
                        unique_identifier = "%s, <%s:%s>" % (
                            unique_identifier, key, fetch_obj.__dict__.get(key))

            else:
                for obj in base_model_obj_list:
                    for key in unique_keys:
                        fetch_params[key] = obj.__dict__.get(key)
                    fetch_obj = obj.__class__.fetch(fetch_params)
                    if (fetch_obj):
                        unique_identifier_p = ""
                        for i in range(0, len(unique_keys)):
                            unique_identifier_p = "%s, %s:%s" % (
                                unique_identifier_p, unique_keys[i], obj.__dict__.get(unique_keys[i]))
                        unique_identifier_p = unique_identifier_p[2:]
                        unique_identifier = "%s, <%s>" % (
                            unique_identifier, unique_identifier_p)

            if (unique_identifier):
                unique_identifier = unique_identifier[2:]
                msg = ("Entity <{}> obj add_many {} unique check failed.".format(
                    obj0.entity_cls.__tablename__, unique_identifier))
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=0, msg=msg)

        db_model_obj_list = [obj.to_model(obj._entity_cls, attr_map=obj._key_2_db_attr_map)
                             for obj in base_model_obj_list]
        session.add_all(db_model_obj_list)
        return len(base_model_obj_list)

    @classmethod
    def get(cls, query_map={}, to_user_obj=True, joined_keys=[]) -> List[mgt_c_object]:
        query, p_index, p_size = cls.gen_query(query_map)
        if (joined_keys):
            key2attr = cls._key_2_db_attr_map
            for key in joined_keys:
                query = query.options(joinedload(key2attr.get(key, key)))

        if (p_index):
            rcds = query.limit(p_size).offset(p_size * (p_index - 1))
        else:
            rcds = query.all()
        if (not to_user_obj or not rcds):
            return rcds

        return [cls(rcd) for rcd in rcds]

    @classmethod
    def fetch(cls, query_map={}, to_user_obj=True, joined_keys=[]):
        if (not isinstance(query_map, dict)):
            query_map = {"id": query_map}
        query, p_index, p_size = cls.gen_query(query_map)
        if (joined_keys):
            key2attr = cls._key_2_db_attr_map
            for key in joined_keys:
                query = query.options(joinedload(key2attr.get(key, key)))
        rcd = query.first()
        if (not to_user_obj or not rcd):
            return rcd

        return cls(rcd)

    @classmethod
    def gen_query(cls, query_map={}):
        """
            @Summary :  OrderBy, GroupBy 在gen_query()外部写；
                        关联对象的 joinload(Target) 自己在获取query之后写；
                        page_index(start from 1), page_size 使用本文提供的固定key;

            @query_map items :
                # attr_s = value_list 会被默认处理成 attr in value_list
                "key1" : value
                    .OR.
                "key1" : {
                    "op": <op>,
                    "value": value
                }
                # if op is not given, "op" -> eq

                op:
                    eq 对于 == (default)
                    ne 对于 !=
                    lt 对于 <
                    ge 对于 >=
                    (not)in 对于 (not)in_
                    (not)like 对于 (not)like
                    ilike 对于 ilike
                    between 对于 between
                    等等
        """
        query = cls._entity_cls.query
        page_index = query_map.get("page_index")
        page_size = query_map.get("page_size")
        b_limit = (not (page_index is None and page_size is None))
        if (b_limit):
            if (not page_index):
                page_index = 1
            if (not page_size):
                page_size = 1000
        try:
            query_map.pop("page_index")
            query_map.pop("page_size")
        except Exception:
            pass

        key2attr = cls._key_2_db_attr_map if (
            cls._key_2_db_attr_map is not None) else {}
        joined_rule_keys = []
        for key, op_v in query_map.items():

            if (not key.count(".")):
                # local Cls attr, support multifie attr(s) ends with 's'.
                attr, attr_s, db_key, db_key_s = parse_attr_s(
                    cls._entity_cls, key2attr, key)

                if (not attr):
                    if (db_key_s is None):
                        if (op_v is None and db_key not in cls._null_supported_filter_attrs):
                            continue
                    elif (op_v is None and db_key_s not in cls._null_supported_filter_attrs):
                        continue

                    raise QueryMapFormatException(data={key: op_v})
            else:
                # join pre entity Cls
                #
                key_list = key.split('.')
                join_rule_list, attr, attr_s, db_key, db_keys = \
                    parse_join_rule_n_attr_s(cls._entity_cls, key_list)

                if (not attr):
                    if (db_key_s is None):
                        if (op_v is None and db_key not in cls._null_supported_filter_attrs):
                            continue
                    elif (op_v is None and db_key_s not in cls._null_supported_filter_attrs):
                        continue

                    raise QueryMapFormatException(data={key: op_v})

                # let's join the new exist ones
                for single_rule_key, remote_entity_cls, jointype, join_attr_pairs in join_rule_list:
                    if (single_rule_key in joined_rule_keys):
                        continue
                    else:
                        # we support only one join rule yet
                        if (1 < len(join_attr_pairs)):
                            data = "[%s] to [%s]" % (
                                single_rule_key, str(join_attr_pairs[0]))
                            raise QueryJoinRuleLengthNotSupportException(data)

                        join_func = getattr(query, jointype, None)
                        if (not join_func):
                            raise Exception()

                        rules = []
                        for local_table_col, local_attr, remote_table_col, remote_attr in join_attr_pairs:
                            rules.append(local_attr == remote_attr)

                        query = join_func(remote_entity_cls, *rules)
                        joined_rule_keys.append(single_rule_key)

            # op & value
            op = "eq"
            if (not isinstance(op_v, dict)):
                if (id(attr) != id(attr_s)):
                    # rule is normal match
                    value = op_v
                else:
                    # rule will be list match
                    op = "in"
                    if (isinstance(op_v, fields.Raw)):
                        op_v = op_v.format(op_v.default)

                    if (isinstance(op_v, (list, tuple))):
                        value = op_v
                    else:
                        value = [op_v]
            else:
                try:
                    op = op_v["op"]
                    value = op_v["value"]
                except Exception:
                    raise QueryMapFormatException(data={key: op_v})
            if (isinstance(value, fields.Raw)):
                value = value.format(value.default)

            # skip op_v(None) filters if attribute doesn't support None value filtering process
            # we usually default filter args to None if user did NOT given.
            if (value is None or op_v is None) and (attr not in cls._null_supported_filter_attrs):
                continue

            # filter
            if op == 'in':
                rule = attr.in_(value)
            elif ("between" != op):
                try:
                    op_attr = list(filter(
                        lambda e: hasattr(attr, e % op),
                        ['__%s__', '%s_', '%s']
                    ))[0] % op
                except IndexError:
                    raise QueryMapFormatException(data={key: op_v})

                rule = getattr(attr, op_attr)(value)
            else:
                if (not isinstance(value, (list, tuple)) or 2 > len(value)):
                    raise QueryMapFormatException(data={key: op_v})
                rule = attr.between(value[0], value[1])
            query = query.filter(rule)

        # do limit
        if (b_limit):
            return query, page_index, page_size

        return query, None, None

    @transaction(session=db.session)
    def update(self, session=db.session, unique_keys=[]):
        if (unique_keys):
            fetch_params = {"id": {"op": "ne", "value": self.id}}
            for key in unique_keys:
                fetch_params[key] = self.__dict__.get(key)
            fetch_obj = self.__class__.fetch(fetch_params)
            if (fetch_obj):
                unique_identifier = ""
                for i in range(0, len(unique_keys)):
                    unique_identifier = "%s, %s:%s" % (
                        unique_identifier, unique_keys[i], self.__dict__.get(unique_keys[i]))
                unique_identifier = unique_identifier[2:]
                msg = "Entity <{}> obj update unique <{}> check failed.".format(self.entity_cls.__tablename__,
                                                                                unique_identifier)
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=[self.entity_cls.__tablename__,
                                                                 unique_identifier])

        etty_obj = self.to_model()
        session.merge(etty_obj)
        return etty_obj.id

    @transaction(session=db.session)
    def delete(self, session=db.session):
        id = getattr(self, "id", 0)
        session.delete(self.to_model())
        return id

    @classmethod
    @transaction(session=db.session)
    def delete_many(cls, entity_obj_list, session=db.session):
        del_ids = []
        for obj in entity_obj_list:
            session.delete(obj)
            del_ids.append(getattr(obj, "id", 0))

        return del_ids


def loc_analyze_attr_default_value(rel_dir):
    #
    if (rel_dir.endswith("TOMANY")):
        return []
    elif (rel_dir.endswith("TOONE")):
        return None
    else:
        return None


def parse_attr_s(entity_cls, key2attr_map, key):
    db_key = key2attr_map.get(key, key)
    db_key_s = None
    attr = getattr(entity_cls, db_key, None)
    attr_s = None

    if (not attr and "s" == key[-1]):
        key_s = key[:-1]
        db_key_s = key2attr_map.get(key_s, key_s)
        attr_s = getattr(entity_cls, db_key_s, None)
    if (attr_s):
        attr = attr_s

    return attr, attr_s, db_key, db_key_s


class base_db_update_model(base_db_model):

    def add(self, session=db.session, unique_keys=[]):
        self.operator_id = None
        self.operate_time = datetime.now()
        return super().add(session, unique_keys)

    def add_many(self, session=db.session, unique_keys=[]):
        self.operator_id = None
        self.operate_time = datetime.now()
        return super().add_many(session, unique_keys)

    def update(self, session=db.session, unique_keys=[]):
        self.operator_id = None
        self.operate_time = datetime.now()
        return super().update(session, unique_keys)


def init_db_processors(processor_dir_path, module_name):
    # init db_processor._db_attr_2_key_map
    sub_modules = mgf_match_ls_sub_names(processor_dir_path,
                                         match_exp="^(?!_).+$",
                                         is_path_relative=True, match_opt=0)
    for mod in sub_modules:
        mod_name = mod.split('.')[0]
        db_processor = import_string(
            "app.%s.dao.%s:%s_processor" % (module_name, mod_name, mod_name))
        attr2key_map = db_processor.db_attr_2_key_map()
        table_name = str(db_processor._entity_cls.__tablename__)
        if (attr2key_map and not mgt_c_object._db_model_2_attr2key_map.get(table_name)):
            mgt_c_object._db_model_2_attr2key_map[table_name] = attr2key_map
        g_entity_table_2_processor_map[table_name] = db_processor


def parse_join_rule_n_attr_s(initial_entity_cls, key_list):
    """
    @Return :
        @join_rule_list:
        [
            (
                str0,       # local_table.local_db_key
                <Model>,    # remote entity cls to join
                jointype_str# outerjoin(left) 和 join
                [
                    [
                    str1,   # local db attr key 'table1.key1'
                    attr1,  # 'table1.key1' associated column attribute
                    str2,   # remote db attr key 'table2.key2'
                    attr2,  # 'table2.key2' associated column attribute
                    ],
                    ...
                ]
            ),
            ...
        ],
        @attr,
        @attr_s,
        @db_key,
        @db_key_s
    """
    # init
    join_rule_list = []
    local_entity_cls = initial_entity_cls
    remote_entity_cls = None

    # table join
    for i in range(len(key_list) - 1):
        # ready 4 next
        if (remote_entity_cls):
            local_entity_cls = remote_entity_cls

        #
        key = key_list[i]
        table_name = local_entity_cls.__tablename__
        local_processor = g_entity_table_2_processor_map[table_name]
        local_key2attr = local_processor._key_2_db_attr_map if (
            local_processor._key_2_db_attr_map is not None) else {}
        db_key = local_key2attr.get(key, key)
        remote_entity_cls, jointype, local_remote_join_pairs = parse_join_rule_with_single_remote_table(
            local_processor, local_entity_cls, db_key
        )
        local_table_db_key = "%s.%s" % (table_name, db_key)

        if (not remote_entity_cls):
            msg = ("%s: Join from local db_attr[%s.%s] failed." % (
                RET.INFO(RET.E_ENTITY_AUTO_JOIN_FAILED), table_name, db_key))
            log.error(msg)
            raise EntityAutoJoinFailedException(local_table_db_key)
        if (1 < len(local_remote_join_pairs)):
            msg = "%s" % (
                RET.INFO(RET.E_ORM_JOIN_RULE_LENGTH_NOT_SUPPORTED_ERROR))
            log.error(msg)
            raise QueryJoinRuleLengthNotSupportException(local_table_db_key)

        join_rule_list.append(
            (local_table_db_key, remote_entity_cls,
             jointype, local_remote_join_pairs))

    # last attr
    key = key_list[-1]
    last_table_name = remote_entity_cls.__tablename__
    last_processor = g_entity_table_2_processor_map[last_table_name]
    last_key2attr = last_processor._key_2_db_attr_map if (
        last_processor._key_2_db_attr_map is not None) else {}
    attr, attr_s, db_key, db_key_s = parse_attr_s(
        remote_entity_cls, last_key2attr, key)

    return join_rule_list, attr, attr_s, db_key, db_key_s


def parse_join_rule_with_single_remote_table(db_processor, entity_cls, db_key):
    """
    @return : (Model, <list:<list:str1, attr1, str2, attr2>>)
        @Model : remote entity class
        @str: jointype: 'outerjoin', 'join'
        @str1: local db attr key 'table1.key1'
        @attr1: 'table1.key1' associated column attribute
        @str2: remote db attr key 'table2.key2'
        @attr2: 'table2.key2' associated column attribute
    """

    # init
    remote_entity_cls = None
    jointype = "outerjoin"
    is_innerjoin = False
    local_attr = None
    local_table_key = "%s.%s" % (entity_cls.__tablename__, db_key)
    remote_attr = None
    remote_table_key = ""
    relation_pairs = []

    if (hasattr(entity_cls, db_key)):
        # the db key is there, but no foreign key associated.
        # let's check db_processor
        ex_join_rules = db_processor.ex_join_rules()
        if (db_key in ex_join_rules):
            join_rule = ex_join_rules[db_key]
            remote_entity_cls = join_rule["remote_entity_cls"]
            jointype = join_rule["type"]
            if (hasattr(entity_cls, db_key)):
                local_attr = getattr(entity_cls, db_key)
            else:
                raise Exception()
            remote_db_key = join_rule["remote_db_key"]
            if (hasattr(remote_entity_cls, remote_db_key)):
                remote_attr = getattr(remote_entity_cls, remote_db_key)
            else:
                raise Exception()
            remote_table_key = "%s.%s" % (
                remote_entity_cls.__table__name, remote_db_key)

            relation_pairs.append(
                [local_table_key, local_attr, remote_table_key, remote_attr])
        else:
            #
            join_relations = inspect(entity_cls).relationships
            tar_relation = getattr(join_relations, db_key, None)
            if (not tar_relation):
                # there's NO foreign key defined to get this remote entity relation
                raise Exception()
            else:
                # Use db designed join attrss
                local_remote_pairs = tar_relation.local_remote_pairs
                for pair_local, pair_remote in local_remote_pairs:
                    local_table_key = "%s.%s" % (
                        pair_local.table.name, pair_local.key)
                    remote_table_key = "%s.%s" % (
                        pair_remote.table.name, pair_remote.key)

                    local_entity_cls = g_entity_table_2_processor_map[pair_local.table.name]._entity_cls
                    local_attr = getattr(
                        local_entity_cls, pair_local.key, None)
                    remote_entity_cls = g_entity_table_2_processor_map[pair_remote.table.name]._entity_cls
                    remote_attr = getattr(
                        remote_entity_cls, pair_remote.key, None)

                    if (not is_innerjoin and local_attr):
                        if (not local_attr.expression.nullable):
                            is_innerjoin = True
                            jointype = "join"

                    relation_pairs.append([local_table_key, local_attr,
                                           remote_table_key, remote_attr])
    else:
        raise Exception()

    return remote_entity_cls, jointype, relation_pairs
