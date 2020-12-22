import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_references_outside_of_its_staging_area import (
    no_references_outside_of_its_own_staging_area,
)


@pytest.fixture
def manifest() -> Manifest:
    return Manifest(
        {
            "nodes": {
                "staging_1": {
                    "unique_id": "staging_1",
                    "resource_type": "model",
                    "fqn": ["foo", "staging", "area_1"],
                },
                "staging_2": {
                    "unique_id": "staging_2",
                    "resource_type": "model",
                    "fqn": ["foo", "staging", "area_2"],
                }
            },
            "child_map": {
                "staging_1": ["staging_2"],
                "staging_2": [],
            },
            "disabled": [],
            "sources": {},
        }

    )


def test_no_references_outside_of_its_staging_area(manifest):
    passes, failures = no_references_outside_of_its_own_staging_area(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert pass_ids == ["staging_1"]
    assert failure_ids == ["staging_2"]
