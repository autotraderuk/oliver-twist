# -*- coding: utf-8 -*-
"""Document test_engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:13

"""
from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.engine import RuleEngine
from olivertwist.ruleengine.rule import Rule
from olivertwist.ruleengine.result import Result


def test_rule_engine_returns_results_for_rule_set(empty_raw_manifest):
    failures = [Node({})]
    engine = RuleEngine([Rule("test", "this always fails!", lambda m: ([], failures))])

    results = engine.run(Manifest(empty_raw_manifest))

    assert len(results) == 1
    assert isinstance(results[0], Result)
