# -*- coding: utf-8 -*-
"""Document node here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:56

"""
from copy import deepcopy
from typing import Dict

import networkx as nx


class Manifest:
    def __init__(self, data: Dict[str, Dict]):
        self._data = data
        self._graph = self._generate_graph(data)

    @property
    def graph(self) -> nx.DiGraph:
        return self._graph.copy()

    def nodes(self):
        for node_id in self.graph.nodes:
            yield self.get_node(node_id)

    def get_node(self, node_id: str) -> "Node":
        node_dicts = ["nodes", "exposures", "sources"]

        for node_dict in node_dicts:
            try:
                return Node(self._data[node_dict][node_id])
            except KeyError:
                continue

        for node in self._data["disabled"]:
            if node["unique_id"] == node_id:
                return Node(node)

        raise KeyError(f"node_id '{node_id}' not found")

    @staticmethod
    def _generate_graph(data) -> nx.DiGraph:
        graph = nx.DiGraph()

        for node_id, child_node_ids in data["child_map"].items():
            graph.add_node(node_id)
            for child_node_id in child_node_ids:
                graph.add_edge(node_id, child_node_id)

        return graph


class Node:
    def __init__(self, dbt_node_data: dict):
        self.data = dbt_node_data

    @property
    def id(self) -> str:
        return self.data["unique_id"]

    @property
    def is_enabled(self) -> bool:
        # FIXME: Feels hacky to assume no config means the model is enabled. This was added to make exposures work
        return self.data.get("config", {}).get("enabled", True)

    @property
    def is_mart(self) -> bool:
        return self.data["resource_type"] == "model" and self.__fqn_contains("marts")

    @property
    def is_source(self) -> bool:
        return self.data["resource_type"] == "source"

    @property
    def is_staging(self) -> bool:
        return self.data["resource_type"] == "model" and (
            self.__fqn_contains("staging") or "stg_" in self.id
        )

    def __fqn_contains(self, namespace: str) -> bool:
        return namespace in self.data.get("fqn", [])
