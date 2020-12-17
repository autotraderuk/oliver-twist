import pytest

from olivertwist.manifest import Manifest
from olivertwist.rules.no_rejoin_models import no_rejoin_models


@pytest.fixture
def raw_manifest() -> dict:
    return {
        "nodes": {
            "S": {"unique_id": "S"},
            "D": {"unique_id": "D"},
            "1": {"unique_id": "1"},
            "2": {"unique_id": "2"},
            "3": {"unique_id": "3"},
            "4": {"unique_id": "4"},
        },
        "child_map": {
            "S": ["1"],
            "D": [],
            "1": ["3", "2"],
            "2": ["4", "D"],
            "3": ["D"],
            "4": ["D"],
        },
    }


def test_no_rejoin_models(raw_manifest):
    manifest = Manifest(raw_manifest)

    passes, failures = no_rejoin_models(manifest)

    assert [m.id for m in passes] == ["S", "D", "3", "4"]
    assert [m.id for m in failures] == ["1", "2"]
