# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:45

"""
from pathlib import Path
from typing import List, Union

import olivertwist
from olivertwist.config.model import Config, Severity
from olivertwist.manifest import Manifest
from olivertwist.ruleengine.discovery import rules_in_path
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    @classmethod
    def with_configured_rules(
        cls, config: Config, directory: Union[str, Path] = None
    ) -> "RuleEngine":
        if directory is None:
            directory = Path(olivertwist.__path__[0])

        all_rules = rules_in_path(directory)
        enabled_rules = RuleEngine.__get_enabled_rules(all_rules, config)
        return cls(enabled_rules)

    def run(self, manifest: Manifest) -> List[Result]:
        return [Result(rule, *rule.apply(manifest)) for rule in self.rules]

    def __get_enabled_rules(all_rules: List[Rule], config: Config):
        enabled_rules = []
        for rule in all_rules:
            if rule.id not in config.get_disabled_rule_ids():
                rule_config = config.get_config_for_rule_id(rule.id)
                if rule_config:
                    rule.severity = rule_config.severity
                else:
                    rule.severity = Severity.ERROR
                enabled_rules.append(rule)
        return enabled_rules
