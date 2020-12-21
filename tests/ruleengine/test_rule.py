# -*- coding: utf-8 -*-
""".

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:28

"""
from unittest.mock import Mock

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import Rule


def test_apply_splits_nodes_using_callable(empty_raw_manifest):
    passes = [Node({"original_file_path": "filepath1"})]
    failures = [
        Node({"original_file_path": "filepath2"}),
        Node({"original_file_path": "filepath3"}),
    ]
    dummy_manifest = Manifest(empty_raw_manifest)

    rule = Rule("warning", "basic_rule", lambda _: (passes, failures))
    result = rule.apply(dummy_manifest)

    assert result[0] == passes
    assert result[1] == failures


def test_rule_instances_are_callable(empty_raw_manifest):
    callable = Mock()
    dummy_manifest = Manifest(empty_raw_manifest)

    rule = Rule(id="id", name="basic_rule", func=callable)
    rule(dummy_manifest)

    callable.assert_called_once_with(dummy_manifest)
