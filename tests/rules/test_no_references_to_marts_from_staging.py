import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_references_to_marts_from_staging import (
    no_references_to_marts_from_staging,
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
                "staging_2": {
                    "unique_id": "staging_2",
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
                "staging_1": ["staging_2"],
                "staging_2": [],
                "mart_1": ["staging_1"],
            },
            "disabled": [],
            "sources": {},
        }

    )


def test_no_references_to_marts_from_staging(manifest):
    passes, failures = no_references_to_marts_from_staging(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert pass_ids == ["staging_2", "mart_1"]
    assert failure_ids == ["staging_1"]
