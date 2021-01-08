# -*- coding: utf-8 -*-
"""Auto-magic rule discovery.

Copyright (C) 2021, Auto Trader UK
Created 08. Jan 2021 18:01

"""
import pkgutil
from importlib import import_module

from olivertwist.ruleengine.rule import Rule


def rules_in_package(package):
    rules = []
    for info in pkgutil.walk_packages(
        path=package.__path__, prefix=package.__name__ + "."
    ):
        if "__" in info.name:
            continue

        mod = import_module(info.name)
        for obj in mod.__dict__.values():
            if isinstance(obj, Rule):
                rules.append(obj)

    return rules
