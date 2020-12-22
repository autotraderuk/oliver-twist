# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:45

"""
import pkgutil
from importlib import import_module
from typing import List

import olivertwist
from olivertwist.manifest import Manifest
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def __iter__(self):
        return iter(self.rules)

    @classmethod
    def with_default_rules(cls) -> "RuleEngine":
        rules = cls.__autodiscover_rules_in_package(olivertwist)
        return cls(rules)

    def run(self, manifest: Manifest) -> List[Result]:
        return [Result(rule, *rule.apply(manifest)) for rule in self.rules]

    @classmethod
    def __autodiscover_rules_in_package(cls, package):
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
