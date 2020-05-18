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


# globals
g_static_exclude_attrs = ("metadata", "query", "query_class")


#
__all__ = [
    "mgt_c_base_object",
    "mgt_c_object_from_json"
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


class mgt_c_object_from_json(object):
    # include attribute list, for those attribute who starts with "_"
    # we automatically exclude keys start with "_"
    _include_attr_list = None
    # support attributes, even for those does start with "_".
    _support_attr_list = None
    # while doing __eq__ process, exclude these attributes
    _eq_exclude_attr_list = None

    # user support attribute list, could be reset by reset()
    _user_support_attr_list = None

    def __init__(self, json_obj={}, b_reserve=False):
        self_attrs = [attr for attr in vars(self)
                      if (("_" != attr[:1] or attr in self._include_attr_list)
                          and attr not in g_static_exclude_attrs
                          )]

        # init
        for attr in self_attrs:
            try:
                setattr(self, attr, None)
            except Exception as e:
                print(str(e))

        if (not json_obj or not isinstance(json_obj, dict)):
            return

        if (self._user_support_attr_list is None):
            self._user_support_attr_list = []
        if (self._include_attr_list is None):
            self._include_attr_list = []
        if (self._eq_exclude_attr_list is None):
            self._eq_exclude_attr_list = ["_include_attr_list",
                                          "_support_attr_list",
                                          "_eq_exclude_attr_list"]
        else:
            self._eq_exclude_attr_list += ["_include_attr_list",
                                           "_support_attr_list",
                                           "_eq_exclude_attr_list"]
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

            # for those spoorted attributes but not given, set None
            for key in list(self._support_attr_list):
                if (not hasattr(self, key)):
                    setattr(self, key, None)

    def _local_setattr(self, key, value, b_reserve=False):
        if (not b_reserve or (not isinstance(value, dict)
                              and not isinstance(value, list)
                              and not isinstance(value, tuple))):
            setattr(self, key, value)
        elif (isinstance(value, dict)):
            v_obj = mgt_c_object_from_json(value, b_reserve)
            setattr(self, key, v_obj)
        else:
            if (not value):
                setattr(self, key, value)
                return
            v_list = mgt_c_object_from_json.parse_list(value)
            setattr(self, key, v_list)

    @staticmethod
    def parse_list(value_list):
        if (not value_list):
            return value_list

        v_list = []
        for v in value_list:
            if (not isinstance(v, dict) and not isinstance(v, list) and not isinstance(v, tuple)):
                v_list.append(v)
            elif (isinstance(v, dict)):
                v_obj = mgt_c_object_from_json(v, True)
                v_list.append(v_obj)
            else:
                v_parse = mgt_c_object_from_json.parse_list(v)
                v_list.append(v_parse)

        return v_list

    @staticmethod
    def reverse_parse_list(value_list):
        if (not value_list):
            return value_list

        v_list = []
        for v in value_list:
            if (not isinstance(v, mgt_c_object_from_json) and not isinstance(v, list) and not isinstance(v, tuple)):
                v_list.append(v)
            elif (isinstance(v, mgt_c_object_from_json)):
                v_list.append(v.to_json())
            else:
                v_parse = mgt_c_object_from_json.reverse_parse_list(v)
                v_list.append(v_parse)

        return v_list

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

            # do NOT initialize reset attrs
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
                    if ("_" == attr[:1] or attr in g_static_exclude_attrs):
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
        if ((not isinstance(v, mgt_c_object_from_json))
            and (not isinstance(v, list))
                and (not isinstance(v, tuple))):
            return v
        elif (isinstance(v, mgt_c_object_from_json)):
            return v.to_json()
        else:
            return mgt_c_object_from_json.reverse_parse_list(v)

    def __eq__(self, oth):
        if (not isinstance(oth, mgt_c_object_from_json)):
            return False
        self_attrs = set([attr for attr in vars(self)
                          if ("_" != attr[:1]
                              and attr not in g_static_exclude_attrs
                              )])
        oth_attrs = set([attr for attr in vars(oth)
                         if ("_" != attr[:1]
                             and attr not in g_static_exclude_attrs
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
