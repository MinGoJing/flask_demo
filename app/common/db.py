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
from typing import List
from datetime import datetime

# flask
from flask_restful import fields
from sqlalchemy.inspection import inspect

# base util
from mgutil.base import mgt_c_object
from mgutil.base import g_exclude_attrs_from_db_model
from mgutil.base import attr_list
from mgutil.deco import transaction

# app
from app import db

# local
from .exception import QueryMapFormatException, EntityUpdateUniqueKeyExistsException

# log
import logging
log = logging.getLogger("SYS")

# export
__all__ = [
    "base_db_model",
    "base_db_update_model"
]


class base_db_model(mgt_c_object):
    """
    @Summary: basic ORM entity processor.
            inherit this, and save a lot time in handlering basic AUDS process.

    @_entity_cls: DB entity Class name.
    @_key2attr: dict from key to attribute.
            key is the API feature name;
            attribute is Class member.
    """
    _exclude_attr_list = None
    _entity_cls = None
    _key2attr = None
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
            self._entity_cls, exclude_attrs=self._exclude_attr_list))
        if (self._default_value_map is None):
            self._default_value_map = {}
        if (self._null_supported_filter_attrs is None):
            self._null_supported_filter_attrs = []

        self._dispatch_relation_attr_default_value()

        if (isinstance(key2attr_map, dict)):
            self._key2attr = key2attr_map
        elif (not self._key2attr):
            self._key2attr = {}

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
                msg = "Entity <{}> obj update unique <{}> check failed.".format(self.entity_cls.__tablename__,
                                                                                unique_identifier)
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=[self.entity_cls.__tablename__,
                                                                 unique_identifier])
        etty_obj = self.to_model(self._entity_cls)
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
                msg = "Entity <{}> obj update {} unique check failed.".format(obj0.entity_cls.__tablename__,
                                                                              unique_identifier)
                log.error(msg)
                raise EntityUpdateUniqueKeyExistsException(data=[obj0.entity_cls.__tablename__,
                                                                 unique_identifier])

        db_model_obj_list = [obj.to_model(obj._entity_cls)
                             for obj in base_model_obj_list]
        session.add_all(db_model_obj_list)
        return len(base_model_obj_list)

    @classmethod
    def get(cls, query_map={}, to_user_obj=False) -> List[mgt_c_object]:
        query, p_index, p_size = cls.gen_query(query_map)
        if (p_index):
            rcds = query.limit(p_size).offset(p_size * (p_index - 1))
        else:
            rcds = query.all()
        if (not to_user_obj or not rcds):
            return rcds

        return [cls(rcd) for rcd in rcds]

    @classmethod
    def fetch(cls, query_map={}, to_user_obj=True):
        if (not isinstance(query_map, dict)):
            query_map = {"id": query_map}
        query, p_index, p_size = cls.gen_query(query_map)
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

        for key, op_v in query_map.items():
            if (not key.count(".")):
                # local Cls attr, support multifie attr(s) ends with 's'.
                key2attr = cls._key2attr if (cls._key2attr is not None) else {}
                attr = getattr(cls._entity_cls, key2attr.get(key, key), None)
                attr_s = None

                if (not attr):
                    if ("s" == key[-1]):
                        key_s = key[:-1]
                        attr_s = getattr(
                            cls._entity_cls, key2attr.get(key_s, key_s), None)

                    if (not attr_s):
                        raise QueryMapFormatException(data={key: op_v})
                    else:
                        attr = attr_s
            else:
                # join Cls attr
                #
                key_list = key.split('.')
                Cls = globals()[key_list[0]]
                attr = Cls
                for i in range(1, len(key_list)):
                    i_key = key_list[i]
                    attr = getattr(attr, i_key, None)
                    if (not attr):
                        raise QueryMapFormatException(data={key: op_v})

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


class base_db_update_model(base_db_model):

    def update(self, session=db.session, unique_keys=[]):
        self.operator_id = 15
        self.operate_time = datetime.now()
        return super().update(session, unique_keys)
