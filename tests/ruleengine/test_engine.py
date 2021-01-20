# -*- coding: utf-8 -*-
"""Document test_engine here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:13

"""
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

import pytest

from olivertwist.config.model import Config, RuleConfig, Severity
from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.engine import RuleEngine
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


@pytest.fixture(scope="module")
def custom_rule_path():
    temp_dir = mkdtemp()
    yield Path(temp_dir)
    rmtree(temp_dir)


def test_rule_engine_returns_results_for_rule_set(empty_raw_manifest):
    failures = [Node({})]
    engine = RuleEngine([Rule("this always fails!", "test", lambda m: ([], failures))])

    results = engine.run(Manifest(empty_raw_manifest))

    assert len(results) == 1
    assert isinstance(results[0], Result)


def test_rule_engine_factory_method():
    engine = RuleEngine.with_configured_rules(Config(universal=[]))

    count = 0
    for rule in engine:
        assert isinstance(rule, Rule)
        count += 1

    assert count >= 4, "There should be at least 4 rules by default"


def test_rule_engine_factory_method_with_config_filtering_out_disabled_rules():
    engine = RuleEngine.with_configured_rules(
        config=Config(
            universal=[
                RuleConfig(id="no-rejoin-models", enabled=False),
                RuleConfig(id="no-disabled-models", enabled=True),
            ]
        )
    )

    assert "no-rejoin-models" not in [rule.id for rule in engine]


def test_rule_engine_factory_method_with_config_setting_severity():
    engine = RuleEngine.with_configured_rules(
        config=Config(
            universal=[
                RuleConfig(
                    id="no-rejoin-models", enabled=True, severity=Severity.ERROR
                ),
                RuleConfig(
                    id="no-disabled-models", enabled=True, severity=Severity.WARNING
                ),
            ]
        )
    )

    assert ("no-rejoin-models", Severity.ERROR) in [
        (rule.id, rule.severity) for rule in engine
    ]
    assert ("no-disabled-models", Severity.WARNING) in [
        (rule.id, rule.severity) for rule in engine
    ]


def test_rule_engine_factory_from_arbitrary_directory(custom_rule_path):
    with open(custom_rule_path / "my_rule.py", "w") as fh:
        fh.write("from olivertwist.ruleengine.rule import Rule\n\n")
        fh.write(
            'r = Rule("my-custom-rule", "Some custom rule", lambda _: (passes, failures))'
        )

    engine = RuleEngine.with_configured_rules(
        config=Config(universal=[]), directory=custom_rule_path
    )

    assert len(engine) == 1
    assert "my-custom-rule" in (rule.id for rule in engine)
