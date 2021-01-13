# -*- coding: utf-8 -*-
"""Interactive rule configuration.

Copyright (C) 2021, Auto Trader UK
Created 08. Jan 2021 18:24

"""
from operator import attrgetter

from PyInquirer import prompt

import olivertwist
from olivertwist.config.model import Config, RuleConfig
from olivertwist.ruleengine.discovery import rules_in_package


class Configurator:
    @classmethod
    def update(cls, config: Config) -> Config:
        all_rules = rules_in_package(olivertwist)
        disabled = config.get_disabled_rule_ids()
        choices = [
            {
                "name": rule.name,
                "checked": rule.id not in disabled,
            }
            for rule in sorted(all_rules, key=attrgetter("name"))
        ]
        questions = [
            {
                "type": "checkbox",
                "name": "rules",
                "message": "Select rules to enable",
                "choices": choices,
                "validate": cls.__validate,
            }
        ]
        answers = prompt(questions)
        return Config(
            [
                RuleConfig(rule.id, False)
                for rule in all_rules
                if rule.name not in answers["rules"]
            ]
        )

    @classmethod
    def __validate(cls, answer):
        if len(answer) < 1:
            return "You must enable at least one rule."

        return True
