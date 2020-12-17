import pytest


@pytest.fixture
def empty_raw_manifest() -> dict:
    return {
        "nodes": {},
        "child_map": {},
    }
