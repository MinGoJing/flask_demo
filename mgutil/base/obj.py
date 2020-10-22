#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   obj.py
@Desc    :   provide base objects
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   Copyright © since 2020 MinGo All Rights Reserved.
@History :
    1.0: 2020/05/13 21:38, MinGo
          1. Created.

'''

# py
import sys
from datetime import date
from datetime import datetime

# falsk
from flask_restful import fields
from flask_wtf import FlaskForm


# exports
__all__ = [
    "mgt_c_base_object",
    "mgt_c_object",
    "attr_list",
    "g_exclude_attrs_from_db_model",
    "g_exclude_attrs_from_flask_form"
]


class mgt_c_base_object(object):
    _obj_name = "<objName>"

    def __init__(self, name):
        self._obj_name = name
        """ Increment the number of active objects """

    def equal(self, other):
        return (id(self) == id(other))

    @property
    def name(self):
        return self._obj_name

    @name.setter
    def name(self, name):
        self._obj_name = name

    def trace(self, space="    ", trace_list=None):
        if (trace_list is None):
            trace_list = []

        # Avoid endless reserve call
        if self in trace_list:
            print("%s%s%s" % (space, str(self),
                              " has been traced. trace() more? OverWrite trace() for it."))
            return
        trace_list.append(self)

        for property, value in vars(self).items():
            if (not isinstance(value, int) and not isinstance(value, float)):
                # print value NOT in list type
                if not (isinstance(value, list)):
                    print("%s%s%s%s" % (space, property, ":", str(value)))
                else:
                    # print list items at the end
                    print("%s%s%s" % (space, property, ":"))
            else:
                # int or float type print
                print("%s%s%s%s" % (space, property, ":", str(value)))

            # print for list or local defined type
            if (not isinstance(value, list)):
                # local defined type
                if (isinstance(value, mgt_c_base_object)):
                    value.trace(space+"  ", trace_list)
            elif (not isinstance(value, str)):
                # list
                if (0 < len(value)):
                    print("%s%s" % (space, "  [list.start]"))
                    for i in range(len(value)):
                        v = value[i]
                        if (isinstance(v, mgt_c_base_object)):
                            # instance list in local defined type
                            if not (0 == i):
                                print("")  # line feed
                            v.trace(space+"    ", trace_list)
                        # normal list
                        else:
                            print("%s%s" % (space+"    ", v))
                    print("%s%s" % (space, "  [list.end]"))


# globals
g_exclude_attrs_from_db_model = ("metadata", "query", "query_class")
g_exclude_attrs_from_flask_form = ()


class mgt_c_object(object):
    # include attribute list, for those attribute who starts with "_"
    # we automatically exclude keys start with "_"
    _include_attr_list = None
    # support attributes, even for those does start with "_".
    _support_attr_list = None
    #
    _exclude_attr_list = None
    # while doing __eq__ process, exclude these attributes
    _eq_exclude_attr_list = None
    # default attribute value dict
    _default_value_map = None

    # user support attribute list, could be reset by reset()
    _user_support_attr_list = None

    # global shared, defined 4 mgt_c_object reverse init from db entity class
    _table_2_db_attr2key_map = {}  # this is a global map
    _to_model_excelude_db_attr_list = None

    def __init__(self, input_obj={}, b_reserve=False):
        if (self._user_support_attr_list is None):
            self._user_support_attr_list = []
        if (self.__class__._user_support_attr_list is None):
            self.__class__._user_support_attr_list = []
        if (self._include_attr_list is None):
            self._include_attr_list = []
        if (self._exclude_attr_list is None):
            self._exclude_attr_list = []
        if (self._support_attr_list is None):
            self._support_attr_list = []
        if (self._to_model_excelude_db_attr_list is None):
            self._to_model_excelude_db_attr_list = []
        if (self._eq_exclude_attr_list is None):
            self._eq_exclude_attr_list = ["_include_attr_list",
                                          "_support_attr_list",
                                          "_eq_exclude_attr_list"]
        else:
            self._eq_exclude_attr_list += ["_include_attr_list",
                                           "_support_attr_list",
                                           "_eq_exclude_attr_list"]
        if (self._default_value_map is None):
            self._default_value_map = {}

        if (not input_obj or (not isinstance(input_obj, (dict, FlaskForm, mgt_c_object))
                              and not is_db_entity(input_obj))):
            return
        elif (isinstance(input_obj, FlaskForm)):
            if (not self._exclude_attr_list):
                self._exclude_attr_list = g_exclude_attrs_from_flask_form
            else:
                self._exclude_attr_list += list(set(self._exclude_attr_list) &
                                                set(g_exclude_attrs_from_flask_form))
        elif (is_db_entity(input_obj)):
            if (not self._exclude_attr_list):
                self._exclude_attr_list = g_exclude_attrs_from_db_model
            else:
                self._exclude_attr_list += list(set(self._exclude_attr_list) &
                                                set(g_exclude_attrs_from_db_model))

        # init attrs None
        for attr in self.attrs:
            try:
                setattr(self, attr, self._default_value_map.get(attr))
            except Exception as e:
                print(str(e))

        # set value
        if (isinstance(input_obj, dict)):
            self._local_json_init(input_obj, b_reserve)
        elif (is_db_entity(input_obj)):
            self._local_model_init(input_obj, b_reserve)
        elif (isinstance(input_obj, FlaskForm)):
            self._local_form_init(input_obj, b_reserve)
        elif (isinstance(input_obj, mgt_c_object)):
            self._local_json_init(input_obj.to_json(), b_reserve)

    def _local_json_init(self, json_obj, b_reserve):
        if (not self._support_attr_list):
            self._support_attr_list = []
            for key, value in json_obj.items():
                self._local_setattr(key, value, b_reserve)
                if ("_" == key[:1]):
                    self._include_attr_list.append(key)
        else:
            # handle supported attributes
            local_attrs = self.attrs
            for key, value in json_obj.items():
                if (key in local_attrs):
                    self._local_setattr(key, value, b_reserve)
                    if ("_" == key[:1]):
                        self._include_attr_list.append(key)

    def _local_model_init(self, model_obj, b_reserve):
        attr2key_map = mgt_c_object.db_attr_2_key_map(model_obj)

        if (not self._support_attr_list):
            self._support_attr_list = []
            for attr in vars(model_obj):
                key = attr2key_map.get(attr, attr)
                if key in self._exclude_attr_list:
                    continue
                value = getattr(model_obj, attr)
                self._local_setattr(key, value, b_reserve)
                if ("_" == key[:1]):
                    self._include_attr_list.append(key)
        else:
            # handle supported attributes
            local_attrs = self.attrs
            for attr in vars(model_obj):
                key = attr2key_map.get(attr, attr)
                if key in self._exclude_attr_list:
                    continue
                value = getattr(model_obj, attr)
                if (key in local_attrs):
                    self._local_setattr(key, value, b_reserve)
                    if ("_" == key[:1]):
                        self._include_attr_list.append(key)

    def _local_form_init(self, form_obj, b_reserve):
        if (self._support_attr_list is None):
            self._support_attr_list = []
            for key in vars(form_obj):
                if key in self._exclude_attr_list:
                    continue
                value = getattr(form_obj, key)
                self._local_setattr(key, value, b_reserve)
                if ("_" == key[:1]):
                    self._include_attr_list.append(key)
        else:
            # handle supported attributes
            local_attrs = self.attrs
            for key in vars(form_obj):
                if key in self._exclude_attr_list:
                    continue
                value = getattr(form_obj, key)
                if (key in local_attrs):
                    self._local_setattr(key, value, b_reserve)
                    if ("_" == key[:1]):
                        self._include_attr_list.append(key)

    def _local_setattr(self, key, value, b_reserve=False):
        if (not b_reserve or (not isinstance(value, (list, tuple, dict, FlaskForm))
                              and not is_db_entity(value))):
            setattr(self, key, value)
        elif (isinstance(value, (dict, FlaskForm)) or is_db_entity(value)):
            v_obj = mgt_c_object(value, b_reserve)
            setattr(self, key, v_obj)
        else:
            if (not value):
                setattr(self, key, value)
                return
            v_list = mgt_c_object.parse_list(value)
            setattr(self, key, v_list)

    @staticmethod
    def parse_list(value_list):
        if (not value_list):
            return value_list

        v_list = []
        for v in value_list:
            if (not isinstance(v, (list, tuple, dict, FlaskForm))
                    and not is_db_entity(v)):
                v_list.append(v)
            elif (isinstance(v, (dict, FlaskForm)) or is_db_entity(v)):
                v_obj = mgt_c_object(v, True)
                v_list.append(v_obj)
            else:
                v_parse = mgt_c_object.parse_list(v)
                v_list.append(v_parse)

        return v_list

    @staticmethod
    def reverse_parse_list(value_list, to_type="json"):
        if (not value_list):
            return value_list

        v_list = []
        for v in value_list:
            if (not isinstance(v, mgt_c_object)
                and not isinstance(v, list)
                    and not isinstance(v, tuple)):
                v_list.append(v)
            elif (isinstance(v, mgt_c_object)):
                if ("Model" == to_type):
                    v_list.append(v.to_model())
                else:
                    v_list.append(v.to_json())
            else:
                v_parse = mgt_c_object.reverse_parse_list(
                    v, to_type)
                v_list.append(v_parse)

        return v_list

    @property
    def entity_cls(self):
        if (hasattr(self, "_entity_cls")):
            return self._entity_cls
        return None

    @property
    def attrs(self):
        if (self._support_attr_list):
            return list(set(self._support_attr_list) | set(self.__class__._user_support_attr_list))

        return [attr for attr in vars(self)
                if (("_" != attr[:1] or attr in
                     list(set(self._include_attr_list) | set(self.__class__._user_support_attr_list)))
                    and attr not in self._exclude_attr_list
                    )]

    def attr(self, key):
        return getattr(self, key)

    def get(self, key):
        return getattr(self, key, None)

    def items(self):
        return self.to_json().items()

    @classmethod
    def db_attr_2_key_map(cls, entity_instance):
        table_name = entity_instance.__class__.__tablename__
        return cls._table_2_db_attr2key_map.get(table_name, {})

    def attr_update(self, input_obj, b_reserve=False):

        # set value
        if (isinstance(input_obj, dict)):
            self._local_json_init(input_obj, b_reserve)
        elif (is_db_entity(input_obj)):
            self._local_model_init(input_obj, b_reserve)
        elif (isinstance(input_obj, FlaskForm)):
            self._local_form_init(input_obj, b_reserve)

    def sub_feature_fetch(self, key_root=""):
        if (not key_root):
            return self

        if (not isinstance(key_root, (list, tuple, str))):
            return None

        # # TODO: jmj,
        # key_list = []
        # if ()

    @classmethod
    def set_user_attrs(cls, usr_attr_map={}):
        if (not usr_attr_map):
            return False

        if (cls._support_attr_list is None):
            cls._support_attr_list = []
        if (cls._user_support_attr_list is None):
            cls._user_support_attr_list = []
        if (cls._default_value_map is None):
            cls._default_value_map = []

        ex_usr_sup_attrs = list(set(usr_attr_map.keys()) -
                                set(cls._support_attr_list))
        if (ex_usr_sup_attrs):
            cls._support_attr_list += ex_usr_sup_attrs
            cls._user_support_attr_list += ex_usr_sup_attrs

            # init new attr values
            for attr in ex_usr_sup_attrs:
                setattr(cls, attr, None)

        return True

    @classmethod
    def reset_user_attrs(cls):
        if (cls._user_support_attr_list):
            ex_usr_sup_attrs = list(set(cls._user_support_attr_list) &
                                    set(cls._support_attr_list))
            if (ex_usr_sup_attrs):
                cls._support_attr_list = list(set(cls._support_attr_list) -
                                              set(ex_usr_sup_attrs))
                cls._user_support_attr_list = []

            # do NOT initialize reset attrs' value
            # we may need them later

        return True

    def to_json(self, json_keys={}):
        j = {}
        if json_keys:
            for key, attr in json_keys.items():
                j[attr] = self._local_json_parse(key)
        else:
            local_attrs = self.attrs
            for attr in vars(self):
                if (attr in local_attrs):
                    j[attr] = self._local_json_parse(attr)
        return j

    def _local_json_parse(self, attr):
        if (not hasattr(self, attr)):
            return None

        v = getattr(self, attr)
        if (not isinstance(v, (mgt_c_object, list, tuple))):
            # # open it when we must do date format translate
            # if isinstance(v, datetime):
            #     return v.strftime('%Y-%m-%d %H:%M:%S')
            # elif isinstance(v, date):
            #     return v.strftime('%Y-%m-%d')
            return v
        elif (isinstance(v, mgt_c_object)):
            return v.to_json()
        else:
            return mgt_c_object.reverse_parse_list(v)

    def to_model(self, model_cls=None, attr_map: dict = {}):
        if (model_cls is None):
            model_cls = self.entity_cls

        attr_dict = {}

        if (self._support_attr_list):
            for key in vars(self):
                attr = attr_map.get(key, key)
                if (key in self._support_attr_list
                        and attr not in self._to_model_excelude_db_attr_list):
                    attr_dict[attr] = self._local_model_parse(key)

        else:
            for key in vars(self):
                attr = attr_map.get(key, key)
                if ("_" == key[:1] or key in self._exclude_attr_list):
                    if (self._include_attr_list):
                        if (key not in self._include_attr_list):
                            continue
                    else:
                        continue
                if (hasattr(model_cls, attr)
                        and attr not in self._to_model_excelude_db_attr_list):
                    attr_dict[attr] = self._local_model_parse(key)

        real_dict = {key: value for key, value in attr_dict.items()
                     if (value or (not value and not (value is None)
                                   and not isinstance(value, (list, dict, tuple))))}
        m = model_cls(**real_dict)
        return m

    def _local_model_parse(self, attr):
        if (not hasattr(self, attr)):
            return self._default_value_map.get(attr)

        v = getattr(self, attr)
        if ((not isinstance(v, (mgt_c_object, list, tuple)))):
            if (not isinstance(v, fields.Raw)):
                return v
            return v.format(v.default)
        elif (isinstance(v, mgt_c_object)):
            return v.to_model()
        else:
            if (not v):
                return v
            return mgt_c_object.reverse_parse_list(v, "Model")

    def __eq__(self, oth):
        if (not isinstance(oth, mgt_c_object)):
            return False
        self_attrs = set([attr for attr in vars(self)
                          if ("_" != attr[:1]
                              and attr not in self._exclude_attr_list
                              )])
        oth_attrs = set([attr for attr in vars(oth)
                         if ("_" != attr[:1]
                             and attr not in self._exclude_attr_list
                             )])
        if (self._include_attr_list):
            self_attrs += set(self._include_attr_list)
        if (oth._include_attr_list):
            oth_attrs += set(oth._include_attr_list)

        if (self._eq_exclude_attr_list):
            self_attrs -= set(self._eq_exclude_attr_list)
        if (oth._eq_exclude_attr_list):
            oth_attrs -= set(oth._eq_exclude_attr_list)

        if (self_attrs ^ oth_attrs):
            return False
        else:
            for attr in self_attrs:
                if (getattr(self, attr) != getattr(oth, attr)):
                    return False

            return True

    def __str__(self):
        attr_list = self.attrs
        fmt_values = []

        if (hasattr(self, "_entity_cls")):
            unique_key_list = getattr(self, "_unique_user_key_list", None)
            if (unique_key_list):
                attr_list = unique_key_list
            fmt_str = "Entity<{} :: {}>"
            if (self.entity_cls):
                fmt_values.append(self.__class__.tablename())
            else:
                fmt_values.append(str(self.__class__))
        else:
            pass

        attr_str = ""
        for key in attr_list:
            attr_str = "%s, %s:%s" % (
                attr_str, key, self.__dict__[key])
        fmt_values.append(attr_str[2:] if (2 < len(attr_str)) else attr_str)

        return fmt_str.format(*fmt_values)


def attr_list(cls, include_attrs=[], exclude_attrs=[],
              attr2key_map={}, entity_relation_backref_attrs=[],
              b_skip_sys_module=False):
    key_list = []

    for attr in dir(cls):
        key = attr2key_map.get(attr, attr)
        if (("_" != key[:1] or key in include_attrs)
                and (key not in exclude_attrs)):
            key_list.append(key)

    for attr in entity_relation_backref_attrs:
        key = attr2key_map.get(attr, attr)
        key_list.append(key)

    # skip attrs from system or third installed module
    if (b_skip_sys_module):
        from werkzeug.utils import import_string
        sys_base_path = sys.base_prefix
        for i in range(len(key_list)-1, -1, -1):
            key = key_list[i]
            var = getattr(cls, key)
            var_mod_file = ""
            var_str = str(var)

            if (var_str.count('(built-in)')):
                key_list.remove(key_list[i])
                continue
            elif (var_str.count(sys_base_path)):
                key_list.remove(key_list[i])
                continue

            # skip basic type instance
            if (isinstance(var, (int, bool, float, str,
                                 dict, tuple, list))):
                continue

            try:
                # skip class instance, but NOT function
                if (hasattr(var, "__class__") and isinstance(getattr(var, "__class__"), type) and
                        (not str(getattr(var, "__class__")).count("<class 'function'>"))):
                    continue

                # handle module directly
                var_mod_file = getattr(var, "__file__")
            except Exception as e:
                e = e
                if (not hasattr(var, "__module__")):
                    continue

                # handle import module secondly
                var_module = getattr(var, "__module__")
                fea_mod = import_string(var_module)
                var_mod_file = getattr(fea_mod, "__file__")

            if (var_mod_file.startswith(sys_base_path)):
                key_list.remove(key_list[i])

    return key_list


def is_db_entity(input_obj):
    return hasattr(input_obj, "__tablename__")
