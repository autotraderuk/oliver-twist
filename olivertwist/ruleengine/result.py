# -*- coding: utf-8 -*-
"""Document result here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 17:09

"""
from typing import List

from olivertwist.config.model import Severity
from olivertwist.manifest import Node
from olivertwist.ruleengine.rule import Rule


class Result:
    def __init__(self, rule: Rule, passes: List[Node], failures: List[Node]):
        self.rule = rule
        self.passes = passes
        self.failures = failures

    @property
    def has_errors(self):
        return self.rule.severity is Severity.ERROR and bool(self.failures)

    @property
    def has_warnings(self):
        return self.rule.severity is Severity.WARNING and bool(self.failures)
