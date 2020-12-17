import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.staging_has_single_source import (
    staging_models_have_single_source,
)


@pytest.fixture
def manifest() -> Manifest:
    return Manifest(
        {
            "nodes": {
                "a": {
                    "unique_id": "a",
                    "fqn": ["a"],
                    "resource_type": "source",
                },
                "staging.b": {
                    "unique_id": "staging.b",
                    "fqn": ["staging", "b"],
                    "resource_type": "model",
                },
                "x": {
                    "unique_id": "x",
                    "fqn": ["x"],
                    "resource_type": "source",
                },
                "y": {
                    "unique_id": "y",
                    "fqn": ["y"],
                    "resource_type": "source",
                },
                "staging.z": {
                    "unique_id": "staging.z",
                    "fqn": ["staging", "z"],
                    "resource_type": "model",
                },
            },
            "child_map": {
                "a": ["staging.b"],
                "staging.b": [],
                "x": ["staging.z"],
                "y": ["staging.z"],
                "staging.z": [],
            },
            "disabled": [],
            "sources": {
                "a": {},
                "x": {},
                "y": {},
            },
        }
    )


def test_staging_models_have_single_source_returns_correct_split(manifest):
    passes, failures = staging_models_have_single_source(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert pass_ids == ["a", "staging.b", "x", "y"]
    assert failure_ids == ["staging.z"]
