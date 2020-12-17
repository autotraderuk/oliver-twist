# -*- coding: utf-8 -*-
""".

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:28

"""
from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import Rule


def test_apply_splits_nodes_using_callable(empty_raw_manifest):
    passes = [Node({"original_file_path": "filepath1"})]
    failures = [
        Node({"original_file_path": "filepath2"}),
        Node({"original_file_path": "filepath3"}),
    ]
    dummy_manifest = Manifest(empty_raw_manifest)

    rule = Rule("basic_rule", "warning", lambda _: (passes, failures))
    result = rule.apply(dummy_manifest)

    assert result[0] == passes
    assert result[1] == failures
