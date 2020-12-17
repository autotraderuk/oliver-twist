# -*- coding: utf-8 -*-
"""Models should not be rejoined downstream

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 17:40

"""
from itertools import product
from typing import List, Tuple

from networkx import DiGraph, all_simple_paths

from olivertwist.manifest import Manifest, Node
from olivertwist.rules.utils import partition


def __find_rejoin_nodes(digraph: DiGraph):
    source_nodes = []
    target_nodes = []
    for n in list(digraph.nodes):
        if digraph.in_degree(n) == 0 and digraph.out_degree(n) >= 1:
            source_nodes.append(n)
        if digraph.in_degree(n) >= 1 and digraph.out_degree(n) == 0:
            target_nodes.append(n)

    rejoin_nodes = set()
    for s, t in list(product(source_nodes, target_nodes)):
        possible_paths = []
        for path in all_simple_paths(digraph, source=s, target=t):
            possible_paths.append(path)
        if len(possible_paths) > 1:
            # rejoin as there is more than one path between two nodes
            tmp = DiGraph()
            for paths in possible_paths:
                # build a graph from the possible paths
                for i in range(1, len(paths)):
                    tmp.add_edge(paths[i - 1], paths[i])
            for node in list(tmp.nodes):
                # rejoin nodes must have an out degree greater than one
                if tmp.out_degree(node) > 1:
                    rejoin_nodes.add(node)
    return rejoin_nodes


def no_rejoin_models(
    manifest: Manifest,
) -> Tuple[List[Node], List[Node]]:
    rejoin_nodes = __find_rejoin_nodes(manifest.graph)

    def is_rejoin_node(node: Node):
        return node.id in rejoin_nodes

    passes, failures = partition(is_rejoin_node, manifest.nodes())
    return list(passes), list(failures)
