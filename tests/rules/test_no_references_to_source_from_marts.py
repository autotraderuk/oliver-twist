import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_references_to_source_from_marts import (
    no_references_to_source_from_marts,
)


@pytest.fixture
def manifest() -> Manifest:
    return Manifest(
        {
            "nodes": {
                "staging_1": {
                    "unique_id": "staging_1",
                    "resource_type": "model",
                    "fqn": ["foo", "staging", "bar"],
                },
                "mart_1": {
                    "unique_id": "mart_1",
                    "resource_type": "model",
                    "fqn": ["foo", "marts", "bar"],
                },
            },
            "child_map": {
                "source_1": ["mart_1"],
                "staging_1": [],
                "mart_1": [],
            },
            "disabled": [],
            "sources": {
                "source_1": {
                    "unique_id": "source_1",
                    "resource_type": "source",
                    "fqn": ["foo", "bar"],
                },
            },
        }

    )


def test_no_references_to_source_from_marts(manifest):
    passes, failures = no_references_to_source_from_marts(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert pass_ids == ["source_1", "staging_1"]
    assert failure_ids == ["mart_1"]
