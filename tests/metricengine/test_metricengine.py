# -*- coding: utf-8 -*-
"""Document test_engine here.

Copyright (C) 2020, Auto Trader UK
Created 16. Dec 2020 16:30

"""
import pytest

from olivertwist.manifest import Manifest, Node
from olivertwist.metricengine.engine import MetricEngine
from olivertwist.metricengine.engine import MetricResult


@pytest.fixture
def raw_manifest() -> dict:
    return {
        "nodes": {
            "S": {"unique_id": "S"},
            "D": {"unique_id": "D"},
            "1": {"unique_id": "1"},
        },
        "child_map": {
            "S": ["1"],
            "D": [],
            "1": ["D"],
        },
    }


def test_metric_engine_returns_results(raw_manifest):
    manifest = Manifest(raw_manifest)

    results = MetricEngine().run(manifest)

    assert len(results) == 3
