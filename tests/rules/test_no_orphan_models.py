# -*- coding: utf-8 -*-
"""Document test_no_orphan_models here.

Copyright (C) 2020, Auto Trader UK
Created 16. Dec 2020 12:51

"""
import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_orphaned_models import no_orphaned_models


@pytest.fixture
def manifest() -> Manifest:
    return Manifest(
        {
            "nodes": {
                "stg_a": {"unique_id": "stg_a", "resource_type": "model"},
                "stg_x": {"unique_id": "stg_x", "resource_type": "model"},
            },
            "child_map": {
                "source_a": ["stg_a"],
                "stg_a": [],
                "stg_x": [],
            },
            "disabled": [],
            "sources": {
                "source_a": {"unique_id": "source_a", "resource_type": "source"},
            },
        }
    )


def test_no_orphaned_models_generates_correct_split(manifest):
    passes, failures = no_orphaned_models(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert failure_ids == ["stg_x"]
    assert pass_ids == ["source_a", "stg_a"]
