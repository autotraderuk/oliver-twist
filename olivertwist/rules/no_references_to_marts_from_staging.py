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
    id="no-references-to-marts-from-staging", name="No references to marts from staging"
)
def no_references_to_marts_from_staging(
    manifest: Manifest,
) -> Tuple[List[Node], List[Node]]:
    def staging_depends_on_mart(node: Node):
        mart_refs = [
            p
            for p in manifest.graph.predecessors(node.id)
            if manifest.get_node(p).is_mart
        ]
        return node.is_staging and len(list(mart_refs)) > 0

    passes, failures = partition(staging_depends_on_mart, manifest.nodes())
    return list(passes), list(failures)
