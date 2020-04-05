#!/usr/bin/python

import os
import json
import random
from urllib.parse import urlparse
import requests
import re


import copy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

UPPER_CASE = 'UPPER_CASE'
LOWER_CASE = 'LOWER_CASE'
NO_CASE = 'NO_CASE'

try:
    from collections.abc import MutableMapping  # noqa
except ImportError:
    from collections import MutableMapping  # noqa

from abc import ABCMeta
from pprint import pformat

class _Dict(dict):
    def __setattr__(self, k, v):
        self[k] = v
    
    def __getattr__(self, k):
        return self[k]

class FieldMeta(ABCMeta):
    Keys = _Dict()
    Defaults = _Dict()
    def __new__(mcs, class_name, bases, attrs):
        reserved = ['Keys', 'Defaults']
        for K in reserved:
            if K in attrs:
                raise AttributeError("'%s' is a reserved attribute for class '%s'. Please do not redefine it." % (K, class_name,))
        cls = super(FieldMeta, mcs).__new__(mcs, class_name, bases, attrs)
        
        def make_fget(n, cls, var_name,):
            def fget(self):
                return getattr(self, var_name, cls.Defaults[n])
            return fget
        
        def make_fset(var_name):
            def fset(self, value):
                setattr(self, var_name, value)
            return fset

        keywords_classes = ['Keywords', 'KeywordsRO']
        for klass_name in keywords_classes:
            if klass_name.endswith('RO'):
                readonly = True
            else:
                readonly = False

            if klass_name in dir(cls):
                klass = getattr(cls, klass_name)
                for n in dir(klass):
                    if not n.startswith('_'):
                        v = getattr(klass, n)
                        cls.Keys[n] = n
                        cls.Defaults[n] = v
                        var_name = '_' + n
                        if readonly:
                            fset = None
                        else:
                            fset = make_fset(var_name)
                        fget = make_fget(n, cls, var_name)
                        setattr(cls, n, property(fget=fget, fset=fset))

        return cls

class FieldBase():
    pass


class Field0(FieldBase, metaclass=FieldMeta):pass

class Field(Field0):
    class Keywords():
        dtype = str

class Field1(Field):
    class Keywords():
        dval = "Hon"
    
    class KeywordsRO():
        author = 'Jahid'

d = Field1()
print(dir(d))
d.dtype = bool
# d.author = 'Jahid'
Field1.Defaults.author = "Hamid"


print(Field1.Defaults.dtype)
print(d.dtype)
print(Field1.Keys.dtype)
print(Field1.Defaults.dval)
print(Field1.Keys.dval)
print(d.author)
# print(Field1.Defaults.name)

class classproperty:
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class C(object):

    @property
    def x(self):
        return 1


a = C()
del a.x