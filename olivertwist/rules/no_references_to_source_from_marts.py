# -*- coding: utf-8 -*-
"""Staging models should have a single source.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 08:40

"""

from typing import List, Tuple

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import rule
from olivertwist.rules.utils import partition


@rule(
    id="no-references-to-source-from-marts", name="No references to source from marts"
)
def no_references_to_source_from_marts(
    manifest: Manifest,
) -> Tuple[List[Node], List[Node]]:
    def mart_depends_on_source(node: Node):
        source_refs = [
            p
            for p in manifest.graph.predecessors(node.id)
            if manifest.get_node(p).is_source
        ]
        return node.is_mart and len(list(source_refs)) > 0

    passes, failures = partition(mart_depends_on_source, manifest.nodes())
    return list(passes), list(failures)
