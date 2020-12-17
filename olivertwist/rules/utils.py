# -*- coding: utf-8 -*-
"""Useful utilities for writing rules.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 17:50

"""
from itertools import filterfalse, tee


def partition(pred, iterable):
    "Use a predicate to partition entries into false entries and true entries."
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)
