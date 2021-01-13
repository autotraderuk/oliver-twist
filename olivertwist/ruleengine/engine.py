# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:45

"""
from typing import List

import olivertwist
from olivertwist.config.model import Config
from olivertwist.manifest import Manifest
from olivertwist.ruleengine.discovery import rules_in_package
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def __iter__(self):
        return iter(self.rules)

    @classmethod
    def with_configured_rules(cls, config: Config) -> "RuleEngine":
        all_rules = rules_in_package(olivertwist)
        rules = [
            rule for rule in all_rules if rule.id not in config.get_disabled_rule_ids()
        ]
        return cls(rules)

    def run(self, manifest: Manifest) -> List[Result]:
        return [Result(rule, *rule.apply(manifest)) for rule in self.rules]
