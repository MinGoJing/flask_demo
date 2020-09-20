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
from werkzeug.utils import import_string

# flask
from flask_restful import fields
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased

# app
from app import db

# mgutil
from mgutil.base import mgt_c_object
from mgutil.base import sub_feature_dict
from mgutil.base import g_exclude_attrs_from_db_model
from mgutil.base import attr_list
from mgutil.deco import transaction
from mgutil.file import mgf_match_ls_sub_names
from mgutil.parser import file_basename_without_suffix

# local
from .func import is_process_failed
from .code import RET
from .exception import GroupByKeyException
from .exception import OrderByKeyException
from .exception import QueryMapFormatException
from .exception import QueryJoinRuleLengthNotSupportException
from .exception import EntityUpdateUniqueKeyExistsException
from .exception import EntityAutoJoinFailedException
from .exception import EntityBackrefAttributeNotFoundException
from .exception import EntityNotFoundException
from .exception import DbEntityInitTableDataNotFoundException
from .exception import InitProcessorNotFoundException
from .exception import DBEntityRemoteReferenceNotMatchException

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "init_db_processors",
    "base_db_processor",
    "base_db_update_processor",
    "base_db_init_processor"
]

# global
g_entity_table_2_processor_map = {}
g_entity_table_2_init_processor_map = {}


class base_db_processor(mgt_c_object):
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
    _unique_user_key_list = None
    _null_supported_filter_db_attrs = None
    _entity_relation_backref_db_attr_list = None
    _entity_relation_fk_ref_db_attr_list = None
    _entity_relation_ref_target_list = None
    _processor_map = {}

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
        if (self._entity_relation_backref_db_attr_list is None):
            self._entity_relation_backref_db_attr_list = []
        if (self._entity_relation_fk_ref_db_attr_list is None):
            self._entity_relation_fk_ref_db_attr_list = []
            self._entity_relation_ref_target_list = []
        if (self._support_attr_list is None):
            self._support_attr_list = []
        self._support_attr_list += set(attr_list(
            self._entity_cls, exclude_attrs=self._exclude_attr_list,
            attr2key_map=self.__class__.db_attr_2_key_map(),
            entity_relation_backref_attrs=self._entity_relation_backref_db_attr_list))
        if (self._default_value_map is None):
            self._default_value_map = {}
        if (self._null_supported_filter_db_attrs is None):
            self._null_supported_filter_db_attrs = []
        if (self._unique_user_key_list is None):
            self._unique_user_key_list = []

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
        if (not self._null_supported_filter_db_attrs):
            return []
        return self._null_supported_filter_db_attrs

    @classmethod
    def ex_join_rules(cls):
        if (hasattr(cls, "_ex_join_rules_from_db_key")):
            return cls._ex_join_rules_from_db_key

        return {}

    @classmethod
    def tablename(cls):
        if (hasattr(cls._entity_cls, "__tablename__")):
            return cls._entity_cls.__tablename__
        return "<tablename not found>"

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
    def add(self, session=db.session, unique_keys=[], do_flush=True):
        if (not unique_keys):
            unique_keys = self._unique_user_key_list
        if (unique_keys):
            fetch_params = {}
            for key in unique_keys:
                fetch_params[key] = self.__dict__.get(key)
            fetch_obj = self.__class__.fetch(fetch_params, session=session)
            if (fetch_obj):
                unique_identifier = ""
                for i in range(0, len(unique_keys)):
                    unique_identifier = "%s, %s:%s" % (
                        unique_identifier, unique_keys[i], self.__dict__.get(unique_keys[i]))
                unique_identifier = unique_identifier[2:]
                raise EntityUpdateUniqueKeyExistsException(
                    (self._entity_cls.__tablename__, unique_identifier))
        etty_obj = self.to_model(attr_map=self._key_2_db_attr_map)
        session.add(etty_obj)
        if (do_flush):
            session.flush()
        return etty_obj.id

    @classmethod
    @transaction(session=db.session)
    def add_many(cls, base_model_obj_list, unique_keys=[], session=db.session, do_flush=False):
        if (not unique_keys):
            unique_keys = cls._unique_user_key_list
        if (unique_keys):
            fetch_params = {}
            unique_identifier = ""
            if (1 == len(unique_keys)):
                key = unique_keys[0]
                fetch_params[key] = {"op": "in",
                                     "value": [obj.__dict__.get(key) for obj in base_model_obj_list]}
                fetch_objs = cls.get(fetch_params, session=session)
                if (fetch_objs):
                    for fetch_obj in fetch_objs:
                        unique_identifier = "%s, <%s:%s>" % (
                            unique_identifier, key, fetch_obj.__dict__.get(key))

            else:
                for obj in base_model_obj_list:
                    for key in unique_keys:
                        fetch_params[key] = obj.__dict__.get(key)
                    fetch_obj = cls.fetch(fetch_params)
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
                raise EntityUpdateUniqueKeyExistsException(
                    data=(cls.tablename(), unique_identifier))

        db_model_obj_list = [obj.to_model(obj._entity_cls, attr_map=obj._key_2_db_attr_map)
                             for obj in base_model_obj_list]
        session.add_all(db_model_obj_list)
        if (do_flush):
            session.flush()
        return len(base_model_obj_list)

    @classmethod
    def get(cls, query_map={}, to_user_obj=True, joined_keys=[],
            group_by=[], order_by=[], session=db.session) -> List[mgt_c_object]:
        query, p_index, p_size, joined_remote_db_attr_map = cls.gen_query(
            query_map, session=session)
        if (joined_keys):
            key2attr = cls._key_2_db_attr_map
            # TODO: jmj, gen join

            for key in joined_keys:
                query = query.options(joinedload(key2attr.get(key, key)))

        # group
        if (group_by):
            group_by_db_attr_list = cls.gen_group(
                query, group_by, joined_remote_db_attr_map, session=session)
            if (group_by_db_attr_list):
                query = query.group_by(*group_by_db_attr_list)

        # order
        if (order_by):
            order_by_db_attr_list = cls.gen_order(
                query, order_by, joined_remote_db_attr_map, session=session)
            if (order_by_db_attr_list):
                query = query.order_by(*order_by_db_attr_list)

        if (p_index):
            rcds = query.limit(p_size).offset(p_size * (p_index - 1))
        else:
            rcds = query.all()
        if (not to_user_obj or not rcds):
            return rcds

        return [cls(rcd) for rcd in rcds]

    @classmethod
    def fetch(cls, query_map={}, to_user_obj=True, joined_keys=[],
              group_by=[], order_by=[], session=db.session):
        if (not isinstance(query_map, dict)):
            query_map = {"id": query_map}
        query, p_index, p_size, joined_remote_db_attr_map = cls.gen_query(
            query_map, session=session)
        if (joined_keys):
            key2attr = cls._key_2_db_attr_map
            for key in joined_keys:
                query = query.options(joinedload(key2attr.get(key, key)))

        # group
        if (group_by):
            group_by_db_attr_list = cls.gen_group(
                query, group_by, joined_remote_db_attr_map, session=session)
            if (group_by_db_attr_list):
                query = query.group_by(*group_by_db_attr_list)

        # order
        if (order_by):
            order_by_db_attr_list = cls.gen_order(
                query, order_by, joined_remote_db_attr_map, session=session)
            if (order_by_db_attr_list):
                query = query.order_by(*order_by_db_attr_list)

        rcd = query.first()
        if (not to_user_obj or not rcd):
            return rcd

        return cls(rcd)

    @classmethod
    def gen_query(cls, query_map={}, session=db.session):
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
        query = session.query(cls._entity_cls)
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
        joined_remote_db_attr_map = {}
        for key, op_v in query_map.items():

            if (not key.count(".")):
                # local Cls attr, support multifie attr(s) ends with 's'.
                attr, attr_s, db_key, db_key_s = parse_attr_s(
                    cls._entity_cls, key2attr, key)

                if (not attr):
                    if (db_key_s is None):
                        if (op_v is None and db_key not in cls._null_supported_filter_db_attrs):
                            continue
                    elif (op_v is None and db_key_s not in cls._null_supported_filter_db_attrs):
                        continue

                    raise QueryMapFormatException(
                        data=(cls.tablename(), "%s: %s" % (key, op_v)))
            else:
                # join pre entity Cls
                #
                key_list = key.split('.')
                join_rule_list, attr, attr_s, db_key, db_keys = parse_join_rule_n_attr_s(
                    cls._entity_cls, key_list, cls._processor_map)

                if (not attr):
                    if (db_key_s is None):
                        if (op_v is None and db_key not in cls._null_supported_filter_db_attrs):
                            continue
                    elif (op_v is None and db_key_s not in cls._null_supported_filter_db_attrs):
                        continue

                    raise QueryMapFormatException(
                        data=(cls.tablename(), "%s: %s" % (key, op_v)))

                # let's join the new exist ones
                for remote_entity_db_attr_path, remote_entity_cls, jointype, join_attr_pairs in join_rule_list:
                    if (remote_entity_db_attr_path in joined_remote_db_attr_map):
                        continue
                    else:
                        # we support only one join rule yet
                        if (1 < len(join_attr_pairs)):
                            data = "[%s.%s] to [%s]" % (
                                cls.tablename(), remote_entity_db_attr_path, str(join_attr_pairs[0]))
                            raise QueryJoinRuleLengthNotSupportException(data)

                        join_func = getattr(query, jointype, None)
                        if (not join_func):
                            raise Exception()

                        rules = []
                        for local_table_col, local_attr, remote_table_col, remote_attr in join_attr_pairs:
                            rules.append(local_attr == remote_attr)

                        query = join_func(remote_entity_cls, *rules)
                        joined_remote_db_attr_map[remote_entity_db_attr_path] = remote_entity_cls

            # op & value
            op = "eq"
            if (not isinstance(op_v, dict)):
                if (id(attr) != id(attr_s)):
                    # rule is normal match
                    value = op_v
                    if (value is None and "eq" == op):
                        op = "is"
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
                    if (value is None and "eq" == op):
                        op = "is"
                except Exception:
                    raise QueryMapFormatException(
                        data=(cls.tablename(), "%s: %s" % (key, op_v)))
            if (isinstance(value, fields.Raw)):
                value = value.format(value.default)

            # skip op_v(None) filters if attribute doesn't support None value filtering process
            # we usually default filter args to None if user did NOT given.
            if (value is None or op_v is None) and (db_key not in cls._null_supported_filter_db_attrs):
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
                    raise QueryMapFormatException(
                        data=(cls.tablename(), "%s: %s" % (key, op_v)))

                rule = getattr(attr, op_attr)(value)
            else:
                if (not isinstance(value, (list, tuple)) or 2 > len(value)):
                    raise QueryMapFormatException(
                        data=(cls.tablename(), "%s: %s" % (key, op_v)))
                rule = attr.between(value[0], value[1])
            query = query.filter(rule)

        # do limit
        if (b_limit):
            return query, page_index, page_size, joined_remote_db_attr_map

        return query, None, None, joined_remote_db_attr_map

    @classmethod
    def gen_group(cls, query, group_by=[], joined_remote_db_attr_map={}, session=db.session):
        #
        group_by_db_attr_list = []
        #
        if (not group_by):
            return group_by_db_attr_list

        key2attr = cls._key_2_db_attr_map if (
            cls._key_2_db_attr_map is not None) else {}
        for key in group_by:

            if (not key.count(".")):
                # local Cls attr, support multifie attr(s) ends with 's'.
                attr, attr_s, db_key, db_key_s = parse_attr_s(
                    cls._entity_cls, key2attr, key)

                if (not attr):
                    raise GroupByKeyException(
                        data=(cls.tablename(), key))

                group_by_db_attr_list.append(attr)
            else:
                # if remote entity cls key path exists, use it
                key_list = key.split('.')
                user_key = key_list[-1]
                remote_entity_key_path = file_basename_without_suffix(key)
                #
                if (remote_entity_key_path in joined_remote_db_attr_map):
                    remote_entity_cls = joined_remote_db_attr_map[remote_entity_key_path]
                    remote_key2attr = remote_entity_cls._key_2_db_attr_map if (
                        remote_entity_cls._key_2_db_attr_map is not None) else {}
                    db_key = remote_key2attr.get(user_key, user_key)
                    attr = getattr(remote_entity_cls, db_key)
                    group_by_db_attr_list.append(attr)
                    continue

                # join pre entity Cls
                #
                join_rule_list, attr, attr_s, db_key, db_keys = parse_join_rule_n_attr_s(
                    cls._entity_cls, key_list, cls._processor_map)

                if (not attr):
                    raise GroupByKeyException(
                        data=(cls.tablename(), key))

                group_by_db_attr_list.append(attr)

                # let's join the new exist ones
                for remote_entity_db_attr_path, remote_entity_cls, jointype, join_attr_pairs in join_rule_list:
                    if (remote_entity_db_attr_path in joined_remote_db_attr_map):
                        continue
                    else:
                        # we support only one join rule yet
                        if (1 < len(join_attr_pairs)):
                            data = "[%s] to [%s]" % (
                                remote_entity_db_attr_path, str(join_attr_pairs[0]))
                            raise QueryJoinRuleLengthNotSupportException(data)

                        join_func = getattr(query, jointype, None)
                        if (not join_func):
                            raise Exception()

                        rules = []
                        for local_table_col, local_attr, remote_table_col, remote_attr in join_attr_pairs:
                            rules.append(local_attr == remote_attr)

                        query = join_func(remote_entity_cls, *rules)
                        joined_remote_db_attr_map[remote_entity_db_attr_path] = remote_entity_cls

        return group_by_db_attr_list

    @classmethod
    def gen_order(cls, query, order_by=[], joined_remote_db_attr_map={}, session=db.session):
        #
        order_by_db_attr_list = []

        #
        if (not order_by):
            return order_by_db_attr_list

        key2attr = cls._key_2_db_attr_map if (
            cls._key_2_db_attr_map is not None) else {}
        for key in order_by:
            order_desc = False
            if ('-' == key[0]):
                order_desc = True
                key = key[1:]

            if (not key.count(".")):
                # local Cls attr, support multifie attr(s) ends with 's'.
                attr, attr_s, db_key, db_key_s = parse_attr_s(
                    cls._entity_cls, key2attr, key)

                if (not attr):
                    raise OrderByKeyException(
                        data=(cls.tablename(), key))

                if (order_desc):
                    attr = attr.desc()
                order_by_db_attr_list.append(attr)
            else:
                # if remote entity cls key path exists, use it
                key_list = key.split('.')
                user_key = key_list[-1]
                remote_entity_key_path = file_basename_without_suffix(key)
                #
                if (remote_entity_key_path in joined_remote_db_attr_map):
                    remote_entity_cls = joined_remote_db_attr_map[remote_entity_key_path]
                    remote_key2attr = remote_entity_cls._key_2_db_attr_map if (
                        remote_entity_cls._key_2_db_attr_map is not None) else {}
                    db_key = remote_key2attr.get(user_key, user_key)
                    attr = getattr(remote_entity_cls, db_key)
                    if (order_desc):
                        attr = attr.desc()
                    order_by_db_attr_list.append(attr)
                    continue

                # join pre entity Cls
                #
                join_rule_list, attr, attr_s, db_key, db_keys = parse_join_rule_n_attr_s(
                    cls._entity_cls, key_list, cls._processor_map)

                if (not attr):
                    raise OrderByKeyException(
                        data=(cls.tablename(), key))

                if (order_desc):
                    attr = attr.desc()
                order_by_db_attr_list.append(attr)

                # let's join the new exist ones
                for remote_entity_db_attr_path, remote_entity_cls, jointype, join_attr_pairs in join_rule_list:
                    if (remote_entity_db_attr_path in joined_remote_db_attr_map):
                        continue
                    else:
                        # we support only one join rule yet
                        if (1 < len(join_attr_pairs)):
                            data = "[%s] to [%s]" % (
                                remote_entity_db_attr_path, str(join_attr_pairs[0]))
                            raise QueryJoinRuleLengthNotSupportException(data)

                        join_func = getattr(query, jointype, None)
                        if (not join_func):
                            raise Exception()

                        rules = []
                        for local_table_col, local_attr, remote_table_col, remote_attr in join_attr_pairs:
                            rules.append(local_attr == remote_attr)

                        query = join_func(remote_entity_cls, *rules)
                        joined_remote_db_attr_map[remote_entity_db_attr_path] = remote_entity_cls

        return order_by_db_attr_list

    @classmethod
    @transaction(session=db.session)
    def update(cls, entity_id, update_dict, session=db.session, unique_keys=[]):
        if (not unique_keys):
            unique_keys = cls._unique_user_key_list
        if (unique_keys):
            fetch_params = {"id": {"op": "ne", "value": entity_id}}
            for key in unique_keys:
                fetch_params[key] = update_dict.get(key)
            fetch_obj = cls.fetch(fetch_params, session=session)
            if (fetch_obj):
                unique_identifier = ""
                for i in range(0, len(unique_keys)):
                    unique_identifier = "%s, %s:%s" % (
                        unique_identifier, unique_keys[i], update_dict.get(unique_keys[i]))
                unique_identifier = unique_identifier[2:]
                msg = "Entity <{}> obj update unique <{}> check failed.".format(cls.tablename(),
                                                                                unique_identifier)
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=(cls.tablename(),
                                                                 unique_identifier))

        entity_obj = cls.fetch(entity_id, to_user_obj=False)
        if (not entity_obj):
            raise EntityNotFoundException((cls.tablename(), entity_id))
        cls._update_entity_attrs(entity_obj, update_dict)
        session.merge(entity_obj)
        return entity_obj.id

    @classmethod
    def _update_entity_attrs(cls, entity_obj, update_dict):
        key2db_attr_map = cls._key_2_db_attr_map

        #
        for key, value in update_dict.items():
            if (key in cls._entity_relation_backref_db_attr_list or
                    key in cls._entity_relation_ref_target_list):
                continue

            db_attr = key2db_attr_map.get(key, key)
            try:
                setattr(entity_obj, db_attr, value)
            except AttributeError as e:
                # TODO: jmj,
                raise (e)
            except Exception as e:
                raise (e)

        return

    @classmethod
    @transaction(session=db.session)
    def delete(cls, entity_id, session=db.session):
        entity_obj = cls.fetch(entity_id, to_user_obj=False)
        if (not entity_obj):
            raise EntityNotFoundException(cls.tablename(), entity_id)
        session.delete(entity_obj)
        return entity_id

    @classmethod
    @transaction(session=db.session)
    def delete_many(cls, entity_obj_list, session=db.session):
        del_ids = []
        for obj in entity_obj_list:
            del_ids.append(getattr(obj, "id", 0))
            session.delete(obj)

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


def init_db_processors(processor_dir_path, module_name, init_submod_list=[],
                       processor_map=g_entity_table_2_processor_map,
                       init_processor_map=g_entity_table_2_init_processor_map,
                       b_do_init_processor_init=False):
    # init db_processor._db_attr_2_key_map
    sub_modules = mgf_match_ls_sub_names(processor_dir_path,
                                         match_exp="^(?!_).+$",
                                         is_path_relative=True, match_opt=0)
    if（not init_submod_list and b_do_init_processor_init):
        for mod in sub_modules:
            mod_name=mod.split('.')[0]
            init_submod_list.append(mod_name)

    # init entity backref attrs
    # "table_name" : {
    #   "processor": db_processor cls,
    #   "attr_list": <list:str>
    #   "attr_default_value_list": <list:(None|[])>
    # }
    for mod in sub_modules:
        # iterate db_processor
        mod_name=mod.split('.')[0]
        db_processor=import_string(
            "%s.%s:%s_processor" % (module_name, mod_name, mod_name))
        if (not db_processor):
            msg=("Please define db_processor LIKE ${filename_base}_processor. "
                   "We'll do some init for your db_processor.")
            raise Exception(msg)
        init_processor(db_processor, processor_map)
        # db init processor
        if (init_submod_list is None):
            continue
        if (mod_name in init_submod_list or not init_submod_list):
            db_init_processor=import_string(
                "%s.%s:%s_init_processor" % (module_name, mod_name, mod_name))
            if (not db_init_processor):
                msg = ("Please define db_processor LIKE ${filename_base}_init_processor. "
                       "We'll do some init for your db_processor.")
                log.warning(msg)
            else:
                init_processor(db_init_processor, init_processor_map)

    return


def init_processor(db_processor, processor_map):
    # init db_processor 2 db_attr2key map
    attr2key_map = db_processor.db_attr_2_key_map()
    table_name = str(db_processor._entity_cls.__tablename__)
    if (attr2key_map and not mgt_c_object._table_2_db_attr2key_map.get(table_name)):
        mgt_c_object._table_2_db_attr2key_map[table_name] = attr2key_map
    # init tablename 2 db_processor map
    processor_map[table_name] = db_processor
    db_processor._processor_map = processor_map

    # init backref db keys
    relation_ships = inspect(db_processor._entity_cls).relationships
    if (db_processor._entity_relation_backref_db_attr_list is None):
        db_processor._entity_relation_backref_db_attr_list = []
    if (db_processor._entity_relation_fk_ref_db_attr_list is None):
        db_processor._entity_relation_fk_ref_db_attr_list = []
        db_processor._entity_relation_ref_target_list = []
    for tar_relation in relation_ships:
        if (not tar_relation.backref):
            db_processor._entity_relation_backref_db_attr_list.append(
                tar_relation.key)
        else:
            db_processor._entity_relation_fk_ref_db_attr_list.append(
                "%s_id" % tar_relation.key)
            db_processor._entity_relation_ref_target_list.append(
                tar_relation.key)

    db_processor._entity_relation_backref_db_attr_list = list(
        set(db_processor._entity_relation_backref_db_attr_list))
    db_processor._entity_relation_fk_ref_db_attr_list = list(
        set(db_processor._entity_relation_fk_ref_db_attr_list))
    db_processor._entity_relation_ref_target_list = list(
        set(db_processor._entity_relation_ref_target_list))
    # affect to mgt_c_object._to_model_excelude_db_attr_list
    if (not db_processor._to_model_excelude_db_attr_list):
        db_processor._to_model_excelude_db_attr_list = db_processor._entity_relation_backref_db_attr_list
    else:
        db_processor._to_model_excelude_db_attr_list += db_processor._entity_relation_backref_db_attr_list

    # init db_processor _unique_user_key_list
    uq_user_keys = []
    entity_cls = db_processor._entity_cls
    db_attrs = attr_list(entity_cls,
                         include_attrs=[],
                         exclude_attrs=[] if (
                             db_processor._exclude_attr_list is None) else db_processor._exclude_attr_list,
                         attr2key_map={},
                         entity_relation_backref_attrs=[])
    for db_attr in db_attrs:
        col = getattr(entity_cls, db_attr, None)
        if (not col):
            continue
        if (hasattr(col, "comparator") and hasattr(col.comparator, "unique")):
            if (col.comparator.unique):
                uq_user_keys.append(attr2key_map.get(db_attr, db_attr))
    if (db_processor._unique_user_key_list):
        pass
    elif (1 == len(uq_user_keys)):
        db_processor._unique_user_key_list = uq_user_keys
    elif (hasattr(entity_cls, "__table_args__")):
        uq_user_keys = []
        for arg in entity_cls.__table_args__:
            if (str(arg).startswith("Index(")):
                for col in arg.columns:
                    uq_user_keys.append(attr2key_map.get(col.key, col.key))
            break
        log.warning("Auto detected processor<{}> unique keys<{}>".format(
            entity_cls.__tablename__, str(uq_user_keys)))
        db_processor._unique_user_key_list = uq_user_keys

    return


def parse_join_rule_n_attr_s(initial_entity_cls, key_list, processor_map):
    """
    @Return :
        @join_rule_list:
        [
            (
                str0,       # Entity key path
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
    remote_entity_cls_key_path = ""

    # table join
    for i in range(len(key_list) - 1):
        # ready 4 next
        if (remote_entity_cls):
            local_entity_cls = remote_entity_cls

        #
        key = key_list[i]
        table_name = local_entity_cls.__tablename__
        local_processor = processor_map[table_name]
        local_key2attr = local_processor._key_2_db_attr_map if (
            local_processor._key_2_db_attr_map is not None) else {}
        db_key = local_key2attr.get(key, key)
        remote_entity_cls, jointype, local_remote_join_pairs = parse_join_rule_with_single_remote_table(
            local_processor, local_entity_cls, db_key, processor_map)
        local_table_db_key = "%s.%s" % (table_name, db_key)
        if (not remote_entity_cls_key_path):
            remote_entity_cls_key_path = "%s.%s" % (
                remote_entity_cls_key_path, key)
        else:
            remote_entity_cls_key_path = key

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
            (remote_entity_cls_key_path, remote_entity_cls,
             jointype, local_remote_join_pairs))

    # last attr
    key = key_list[-1]
    if (not key):
        return join_rule_list, None, None, "", ""
    last_table_name = remote_entity_cls.__tablename__
    last_processor = processor_map[last_table_name]
    last_key2attr = last_processor._key_2_db_attr_map if (
        last_processor._key_2_db_attr_map is not None) else {}
    attr, attr_s, db_key, db_key_s = parse_attr_s(
        remote_entity_cls, last_key2attr, key)

    return join_rule_list, attr, attr_s, db_key, db_key_s


def parse_join_rule_with_single_remote_table(db_processor, entity_cls, db_key, processor_map):
    """
    @return : (Model, str0, <list:<list:str1, attr1, str2, attr2>>)
        @Model : remote entity class
        @str0: jointype: 'outerjoin'(leftjoin), 'join'
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

    ex_join_rules = db_processor.ex_join_rules()
    if (hasattr(entity_cls, db_key) or ex_join_rules):
        # the db key is there, but no foreign key associated.
        # let's check db_processor
        if (db_key in ex_join_rules):
            join_rule = ex_join_rules[db_key]
            remote_entity_cls = join_rule["remote_entity_cls"]
            remote_entity_cls = aliased(remote_entity_cls)
            jointype = join_rule["type"]
            if (hasattr(entity_cls, db_key)):
                local_attr = getattr(entity_cls, db_key)
            else:
                raise EntityBackrefAttributeNotFoundException(
                    (entity_cls.tablename(), db_key))
            remote_db_key = join_rule["remote_db_key"]
            if (hasattr(remote_entity_cls, remote_db_key)):
                remote_attr = getattr(remote_entity_cls, remote_db_key)
            else:
                raise Exception()
            remote_table_key = "%s.%s" % (
                remote_entity_cls.__tablename__, remote_db_key)

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
                # Use db designed join attrs
                local_remote_pairs = tar_relation.local_remote_pairs
                for pair_local, pair_remote in local_remote_pairs:
                    local_table_key = "%s.%s" % (
                        pair_local.table.name, pair_local.key)
                    remote_table_key = "%s.%s" % (
                        pair_remote.table.name, pair_remote.key)

                    local_entity_cls = processor_map[pair_local.table.name]._entity_cls
                    local_attr = getattr(
                        local_entity_cls, pair_local.key, None)
                    remote_entity_cls = processor_map[pair_remote.table.name]._entity_cls
                    remote_entity_cls = aliased(remote_entity_cls)
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


class base_db_update_processor(base_db_processor):

    def add(self, session=db.session, unique_keys=[], do_flush=True):
        self.operator_id = None
        self.operate_time = datetime.now()
        return super().add(session, unique_keys=unique_keys, do_flush=do_flush)

    @classmethod
    def add_many(cls, base_model_obj_list, unique_keys=[], session=db.session, do_flush=False):
        now = datetime.now()
        for obj in base_model_obj_list:
            obj.operator_id = None
            obj.operate_time = now
        return super().add_many(base_model_obj_list, unique_keys, session=session, do_flush=do_flush)

    @classmethod
    def update(cls, model_id, up_params: dict, session=db.session, unique_keys=[]):
        if (isinstance(up_params, dict)):
            up_params["operator_id"] = None
            up_params["operate_time"] = datetime.now()
        elif (isinstance(up_params, base_db_processor)):
            up_params.__dict__["operator_id"] = None
            up_params.__dict__["operate_time"] = datetime.now()
        return super().update(model_id, up_params, session=session, unique_keys=unique_keys)


class base_db_init_processor(base_db_processor):
    _init_flag = False
    _table_dependences = []
    # @str1 : {
    #   "remote_table": @str2,
    #   "fetch_key": @str3,
    #   "remote_ref_key": @str4
    # }
    #   @str1: local reference key
    #   @str2: reference table name
    #   @str3: reference table's fetch key
    #   @str4: reference table's reference key, (not given == 'id')
    _reference_key_2_fetch_target = {}
    _autogen_keys = []
    # the columns displayed to user is usually friendly
    #   we should transform them 2 processor key
    _friend_key_2_key_dict = {}

    @classmethod
    def initialize(cls, table_2_datasheet_dict={}, b_db_datasheet=False, b_do_unique_repeat_update=False):
        # if initted, break
        table_name = cls.tablename()
        if (cls._init_flag):
            log.warning("<{}> already initialized, break.".format(table_name))
            return

        # prepare reference table datasheet
        #
        for ref_table_name in cls._table_dependences:
            if (ref_table_name == table_name):
                continue
            remote_db_init_processor = g_entity_table_2_init_processor_map[ref_table_name]
            if (not remote_db_init_processor):
                raise InitProcessorNotFoundException(ref_table_name)
            if (remote_db_init_processor._init_flag):
                continue
            remote_db_init_processor.initialize(
                table_2_datasheet_dict, b_db_datasheet)

        # get datasheet by tablename, and init entity objects
        #
        # get datasheet
        friend_key_2_key_map = cls._friend_key_2_key_dict
        db_attr_2_key_map = cls._db_attr_2_key_map
        if (b_db_datasheet):
            friend_key_2_key_map = db_attr_2_key_map
        datasheet = table_2_datasheet_dict.get(table_name)
        api_datasheet = []
        if (datasheet is None):
            raise DbEntityInitTableDataNotFoundException(table_name)
        elif (not datasheet):
            return
        else:
            # force friend_key -> API_key
            if (cls._friend_key_2_key_dict):
                for data in datasheet:
                    api_datasheet.append({friend_key_2_key_map.get(
                        friend_key, friend_key): value for friend_key, value in data.items()})
            else:
                api_datasheet = datasheet
        # gen entity list
        entity_proc_list = [cls(data) for data in api_datasheet]

        # add(update) entities
        #
        # prepare ref_table's ref_key2(fetch_key2id_dict) map
        ref_key2fetch_dict_map = {}
        for ref_db_attr in cls._entity_relation_fk_ref_db_attr_list:
            ref_key = cls.db_attr_2_key_map().get(ref_db_attr, ref_db_attr)
            # TODO: jmj, auto detect reference table processor
            if (ref_key not in cls._reference_key_2_fetch_target):
                raise Exception(
                    "ref_key<{}> remote tablename NOT given.".format(ref_key))
            # prepare fetch parameter
            fetch_tar = cls._reference_key_2_fetch_target[ref_key]
            fetch_key = fetch_tar.get(
                "fetch_key", fetch_tar.get("remote_ref_key", "id"))
            remote_table_name = fetch_tar["remote_table"]
            ref_init_processor = g_entity_table_2_init_processor_map.get(
                remote_table_name)
            if (not ref_init_processor):
                raise InitProcessorNotFoundException(remote_table_name)
            fetch_values = [getattr(etty, ref_key)
                            for etty in entity_proc_list]
            fetch_values = list(set(fetch_values))
            # filter & gen dict
            ref_entity_objs = ref_init_processor.get(
                {fetch_key+"s": fetch_values})
            if ("id" != fetch_key):
                fetch_key2id_dict = sub_feature_dict(
                    ref_entity_objs, fetch_key, ["id"])
                ref_key2fetch_dict_map[ref_key] = fetch_key2id_dict
        # fix keys need update
        for entity_proc in entity_proc_list:
            # update to remote reference id
            for ref_key in ref_key2fetch_dict_map:
                remote_key = getattr(entity_proc, ref_key)
                if (not remote_key):
                    continue  # ref_id is None
                remote_key2id_dict = ref_key2fetch_dict_map[ref_key]
                remote_id = remote_key2id_dict.get(remote_key)
                if (not remote_id):
                    raise DBEntityRemoteReferenceNotMatchException(
                        (table_name, ref_key, remote_key))
                setattr(entity_proc, ref_key, remote_id)

            # update auto generated local key
            for key in cls._autogen_keys:
                entity_proc.attr_generate(key, getattr(entity_proc, key))

            b_do_add = (entity_proc.id is None)
            if (entity_proc.id):
                if (not entity_proc.fetch(entity_proc.id)):
                    b_do_add = True

            if (b_do_add):
                try:
                    # auto generate key(s) never repeat
                    if (cls._unique_user_key_list and
                            not (set(cls._unique_user_key_list) & set(cls._autogen_keys))):
                        #
                        fetch_p = {}
                        for key in cls._unique_user_key_list:
                            fetch_p[key] = entity_proc.attr(key)
                            
                        fetch_entity = cls.fetch(fetch_p)
                        if (fetch_entity):
                            if (not b_do_unique_repeat_update):
                                log.info("\n    >>--> [EXISTS] "
                                     "%s ." % (str(entity_proc)))
                            else:
                                # attr update value
                                key_set = set(fetch_entity.to_json().keys())
                                key_set = key_set - set(cls._entity_relation_fk_ref_db_attr_list)
                                key_set = key_set - set(cls._entity_relation_ref_target_list)
                                key_set = key_set - set(cls._unique_ser_key_list)
                                
                                for key in key_set:
                                    setattr(fetch_entity, key, entity_proc.attr(key))
                                rcd = cls.update(fetch_entity.id, fetch_entity)
                                
                            continue

                    rcd = entity_proc.add()
                    if (is_process_failed(rcd)):
                        ret, data, msg = rcd.values()
                        if (RET.E_ENTITY_UPDATE_UNIQUE_ERROR == ret):
                            log.warning(msg)
                        else:
                            log.error(msg)
                            raise Exception(msg)
                except Exception as e:
                    if (isinstance(e, EntityUpdateUniqueKeyExistsException)):
                        pass
                    else:
                        raise(e)
            else:
                cls.update(entity_proc.id, entity_proc)

        cls._init_flag = True
        return

    def attr_generate(self, db_attr, *args):
        """
            @: Save db_attr generated value to 'self'
        """
        db_attr = db_attr
        args = args
        return
