# -*- coding: utf-8 -*-
"""Models should have resolvable dependencies.

Copyright (C) 2020, Auto Trader UK
Created 16. Dec 2020 12:53

"""
from typing import List, Tuple

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import rule
from olivertwist.rules.utils import partition


@rule(id="no-orphaned-models", name="No orphaned models allowed")
def no_orphaned_models(manifest: Manifest) -> Tuple[List[Node], List[Node]]:
    """
    return [
        node for node in dbt_manifest_file['nodes'].values()
        if is_staging(node) or is_mart(node)
        if not node['depends_on']['nodes']
    ]
    """

    def is_orphan(node: Node) -> bool:
        dependencies = list(manifest.graph.predecessors(node.id))
        return (node.is_staging or node.is_mart) and len(dependencies) < 1

    passes, failures = partition(is_orphan, manifest.nodes())
    return list(passes), list(failures)
