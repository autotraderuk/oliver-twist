# -*- coding: utf-8 -*-
"""Document test_engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:13

"""
from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.engine import RuleEngine
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


def test_rule_engine_returns_results_for_rule_set(empty_raw_manifest):
    failures = [Node({})]
    engine = RuleEngine([Rule("this always fails!", "test", lambda m: ([], failures))])

    results = engine.run(Manifest(empty_raw_manifest))

    assert len(results) == 1
    assert isinstance(results[0], Result)


def test_rule_engine_factory_method():
    engine = RuleEngine.with_default_rules()

    count = 0
    for count, rule in enumerate(engine):
        assert isinstance(rule, Rule)
        count += 1

    assert count >= 4, "There should be at least 4 rules by default"
