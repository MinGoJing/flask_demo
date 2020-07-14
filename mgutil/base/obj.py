#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   obj.py
@Desc    :   provide base objects
@Version :   1.0
@Author  :   MinGo
@Contact :   mingo_jing@163.com
@License :   (C)Copyright since 2020, MinGo
@History :
    1.0: 2020/05/13 21:38, MinGo
          1. Created.

'''

# py


# falsk
from flask_wtf import FlaskForm


# exports
__all__ = [
    "mgt_c_base_object",
    "mgt_c_object",
    "attr_list",
    "g_exclude_attrs_from_db_model",
    "g_exclude_attrs_from_flask_form"
]


# globals
from flask_sqlalchemy.model import Model


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

    # global shared, defined 4 mgt_c_object reverse init from Model class
    _db_model_2_attr2key_map = {}

    def __init__(self, input_obj={}, b_reserve=False):
        if (self._user_support_attr_list is None):
            self._user_support_attr_list = []
        if (self._include_attr_list is None):
            self._include_attr_list = []
        if (self._exclude_attr_list is None):
            self._exclude_attr_list = []
        if (self._support_attr_list is None):
            self._support_attr_list = []
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

        if (not input_obj or (not isinstance(input_obj, dict)
                              and not (isinstance(input_obj, Model))
                              and not isinstance(input_obj, FlaskForm))):
            return
        elif (isinstance(input_obj, FlaskForm)):
            if (not self._exclude_attr_list):
                self._exclude_attr_list = g_exclude_attrs_from_flask_form
            else:
                self._exclude_attr_list += list(set(self._exclude_attr_list) &
                                                set(g_exclude_attrs_from_flask_form))
        elif (not Model or isinstance(input_obj, Model)):
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
        elif (isinstance(input_obj, Model)):
            self._local_model_init(input_obj, b_reserve)
        elif (isinstance(input_obj, FlaskForm)):
            self._local_form_init(input_obj, b_reserve)

    def _local_json_init(self, json_obj, b_reserve):
        if (not self._support_attr_list):
            self._support_attr_list = []
            for key, value in json_obj.items():
                self._local_setattr(key, value, b_reserve)
                if ("_" == key[:1]):
                    self._include_attr_list.append(key)
        else:
            # handle supported attributes
            for key, value in json_obj.items():
                if (key in list(self._support_attr_list)):
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
            for attr in vars(model_obj):
                key = attr2key_map.get(attr, attr)
                if key in self._exclude_attr_list:
                    continue
                value = getattr(model_obj, attr)
                if (key in list(self._support_attr_list)):
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
            for key in vars(form_obj):
                if key in self._exclude_attr_list:
                    continue
                value = getattr(form_obj, key)
                if (key in list(self._support_attr_list)):
                    self._local_setattr(key, value, b_reserve)
                    if ("_" == key[:1]):
                        self._include_attr_list.append(key)

    def _local_setattr(self, key, value, b_reserve=False):
        if (not b_reserve or (not isinstance(value, (dict, Model, FlaskForm, list, tuple)))):
            setattr(self, key, value)
        elif (isinstance(value, dict) or (isinstance(value, Model))
              or isinstance(value, FlaskForm)):
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
            if ((not isinstance(v, (dict, Model, FlaskForm, list, tuple)))):
                v_list.append(v)
            elif (isinstance(v, (dict, Model, FlaskForm))):
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
        return self._entity_cls

    @property
    def attrs(self):
        if (self._support_attr_list):
            return self._support_attr_list

        return [attr for attr in vars(self)
                if (("_" != attr[:1] or attr in self._include_attr_list)
                    and attr not in self._exclude_attr_list
                    )]

    @classmethod
    def db_attr_2_key_map(cls, entity_instance):
        table_name = entity_instance.__class__.__tablename__
        return cls._db_model_2_attr2key_map.get(table_name, {})

    def set_support_attrs(self, usr_sup_attrs=[]):
        if (not usr_sup_attrs):
            return False

        ex_usr_sup_attrs = list(set(usr_sup_attrs) -
                                set(self._support_attr_list))
        if (ex_usr_sup_attrs):
            self._support_attr_list += ex_usr_sup_attrs
            self._user_support_attr_list += ex_usr_sup_attrs

            # init new attr values
            for attr in ex_usr_sup_attrs:
                setattr(self, attr, None)

        return True

    def reset_support_attrs(self):
        if (self._user_support_attr_list):
            ex_usr_sup_attrs = list(set(self._user_support_attr_list) &
                                    set(self._support_attr_list))
            if (ex_usr_sup_attrs):
                self._support_attr_list = list(set(self._support_attr_list) -
                                               set(ex_usr_sup_attrs))
                self._user_support_attr_list = []

            # do NOT initialize reset attrs' value
            # we may need them later

        return True

    def to_json(self, json_keys={}):
        j = {}
        if json_keys:
            for key, attr in json_keys.items():
                j[attr] = self._local_json_parse(key)
        else:
            for attr in vars(self):
                if (self._support_attr_list):
                    for attr in self._support_attr_list:
                        j[attr] = self._local_json_parse(attr)

                else:
                    if ("_" == attr[:1] or attr in self._exclude_attr_list):
                        if (self._include_attr_list):
                            if (attr not in self._include_attr_list):
                                continue
                        else:
                            continue
                    j[attr] = self._local_json_parse(attr)
        return j

    def _local_json_parse(self, attr):
        if (not hasattr(self, attr)):
            return None

        v = getattr(self, attr)
        if ((not isinstance(v, mgt_c_object))
            and (not isinstance(v, list))
                and (not isinstance(v, tuple))):
            return v
        elif (isinstance(v, mgt_c_object)):
            return v.to_json()
        else:
            return mgt_c_object.reverse_parse_list(v)

    def to_model(self, model_cls=None, attr_map: dict = {}):
        if (model_cls is None):
            model_cls = self.entity_cls
        m = model_cls()
        if attr_map:
            for key, attr in attr_map.items():
                if (hasattr(m, attr)):
                    setattr(m, attr, self._local_model_parse(key))
        else:
            for attr in vars(self):
                if (self._support_attr_list):
                    for attr in self._support_attr_list:
                        setattr(m, attr, self._local_model_parse(attr))

                else:
                    if ("_" == attr[:1] or attr in self._exclude_attr_list):
                        if (self._include_attr_list):
                            if (attr not in self._include_attr_list):
                                continue
                        else:
                            continue
                    if (hasattr(m, attr)):
                        setattr(m, attr, self._local_model_parse(attr))
        return m

    def _local_model_parse(self, attr):
        if (not hasattr(self, attr)):
            return self._default_value_map.get(attr)

        v = getattr(self, attr)
        if ((not isinstance(v, mgt_c_object))
            and (not isinstance(v, list))
                and (not isinstance(v, tuple))):
            return v
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


def attr_list(cls, include_attrs=[], exclude_attrs=[], attr2key_map={}):
    key_list = []

    for attr in dir(cls):
        key = attr2key_map.get(attr, attr)
        if (("_" != key[:1] or key in include_attrs)
                and (key not in exclude_attrs)):
            key_list.append(key)

    return key_list
