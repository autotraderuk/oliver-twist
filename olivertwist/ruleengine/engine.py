# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:45

"""
from typing import List

from olivertwist.manifest import Manifest
from olivertwist.ruleengine.rule import Rule
from olivertwist.ruleengine.result import Result
from olivertwist.rules.no_disabled_models import no_disabled_models
from olivertwist.rules.no_orphaned_models import no_orphaned_models
from olivertwist.rules.staging_has_single_source import (
    staging_models_have_single_source,
)
from olivertwist.rules.no_rejoin_models import no_rejoin_models


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    @classmethod
    def with_default_rules(cls) -> "RuleEngine":
        return cls(
            [
                Rule(
                    name="Disabled models",
                    url="https://github.com/autotraderuk/oliver-twist/blob/main/RULES.md#disabled-models",
                    func=no_disabled_models,
                ),
                Rule(
                    name="No orphaned models",
                    url="https://github.com/autotraderuk/oliver-twist/blob/main/RULES.md#orphaned-models",
                    func=no_orphaned_models,
                ),
                Rule(
                    name="Staging scripts referencing multiple sources",
                    url="https://github.com/autotraderuk/oliver-twist/blob/main/RULES.md#staging-scripts-referencing-multiple-sources",
                    func=staging_models_have_single_source,
                ),
                # Rule(
                #     name="Rejoin models",
                #     url="https://github.com/autotraderuk/oliver-twist/blob/main/RULES.md#rejoin-models",
                #     func=no_rejoin_models,
                # ),
            ]
        )

    def run(self, manifest: Manifest) -> List[Result]:
        return [Result(rule, *rule.apply(manifest)) for rule in self.rules]
