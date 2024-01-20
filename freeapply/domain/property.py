"""freeapply domain property module.
property.py
=========
A function-based module that aims to dynamic domain's properties


Classes:
    ForeignProperty: defines the foreign columns for relationship
    Property: defines each column that use for domain

author: iqpizza6349
"""
from typing import List


class ForeignProperty(object):
    def __init__(self, column: str, ref_column: str, name: str = None):
        self.column = column
        self.ref_column = ref_column
        self.name = name


class Property(object):
    def __init__(self, _type, name: str, foreign_keys: List[ForeignProperty] = None):
        self.type = _type
        self.name = name
        self.foreign = foreign_keys or []






