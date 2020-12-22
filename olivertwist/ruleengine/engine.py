# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:45

"""
from importlib import import_module
from typing import List

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
        rules = cls.__autodiscover_rules_in_package()
        return cls(rules)

    def run(self, manifest: Manifest) -> List[Result]:
        return [Result(rule, *rule.apply(manifest)) for rule in self.rules]

    @staticmethod
    def __autodiscover_rules_in_package():
        rules_package = import_module("olivertwist.rules")
        rules = []
        for module_name, rule_module in rules_package.__dict__.items():
            if not module_name.startswith("__"):
                for obj in rule_module.__dict__.values():
                    if isinstance(obj, Rule):
                        rules.append(obj)
        return rules
