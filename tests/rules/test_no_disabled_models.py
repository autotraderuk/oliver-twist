import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_disabled_models import no_disabled_models


@pytest.fixture
def manifest() -> Manifest:
    return Manifest(
        {
            "nodes": {
                "a": {"unique_id": "a", "config": {"enabled": True}},
                "b": {"unique_id": "b", "config": {"enabled": True}},
            },
            "child_map": {
                "a": [],
                "b": [],
                "x": [],
            },
            "disabled": [
                {"unique_id": "x", "config": {"enabled": False}},
            ],
        }
    )


def test_no_disabled_models_generates_correct_split(manifest):
    passes, failures = no_disabled_models(manifest)

    pass_ids = [p.id for p in passes]
    failure_ids = [f.id for f in failures]

    assert pass_ids == ["a", "b"]
    assert failure_ids == ["x"]
