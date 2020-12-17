import networkx as nx
import pytest

from olivertwist.manifest import Manifest, Node


@pytest.fixture
def raw_manifest() -> dict:
    return {
        "nodes": {
            "a": {"unique_id": "a"},
            "b": {"unique_id": "b"},
            "c": {"unique_id": "c"},
        },
        "child_map": {
            "a": ["b", "c"],
            "b": [],
            "c": [],
            "e": [],
            "s": [],
            "x": [],
        },
        "disabled": [
            {"unique_id": "x"},
        ],
        "exposures": {
            "e": {"unique_id": "e"},
        },
        "sources": {
            "s": {"unique_id": "s"},
        },
    }


def test_nodes_returns_all_nodes(raw_manifest):
    manifest = Manifest(raw_manifest)

    node_ids = [node.id for node in manifest.nodes()]

    assert node_ids == ["a", "b", "c", "e", "s", "x"]


def test_manifest_graph(raw_manifest):
    expected_graph = nx.DiGraph()
    expected_graph.add_edge("a", "b")
    expected_graph.add_edge("a", "c")
    expected_graph.add_node("e")
    expected_graph.add_node("s")
    expected_graph.add_node("x")

    manifest = Manifest(raw_manifest)
    actual_graph = manifest.graph

    assert actual_graph.nodes == expected_graph.nodes
    assert actual_graph.edges == expected_graph.edges


def test_get_node_when_node_is_enabled(raw_manifest):
    manifest = Manifest(raw_manifest)

    node = manifest.get_node("a")

    assert node.id == "a"
    assert isinstance(node, Node)


def test_get_node_when_node_is_disabled(raw_manifest):
    manifest = Manifest(raw_manifest)

    node = manifest.get_node("x")

    assert node.id == "x"
    assert isinstance(node, Node)


def test_get_node_when_node_does_not_exist(raw_manifest):
    manifest = Manifest(raw_manifest)

    with pytest.raises(KeyError):
        manifest.get_node("foo")


def test_node_is_staging_when_in_fqn():
    node = Node(
        {"unique_id": "staging.a", "fqn": ["staging", "a"], "resource_type": "model"}
    )

    assert node.is_staging


def test_node_is_staging_when_prefixed_with_stg():
    node = Node({"unique_id": "stg_a", "fqn": ["stg_a"], "resource_type": "model"})

    assert node.is_staging


def test_node_is_mart_when_in_fqn():
    node = Node(
        {"unique_id": "marts.a", "fqn": ["marts", "a"], "resource_type": "model"}
    )

    assert node.is_mart


def test_node_is_source():
    node = Node({"unique_id": "a", "fqn": ["a"], "resource_type": "source"})

    assert node.is_source
