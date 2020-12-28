# -*- coding: utf-8 -*-
"""Staging models should have a single source.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 10:29

"""

from typing import List, Tuple

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import rule
from olivertwist.rules.utils import partition


@rule(
    id="no-references-outside-of-its-own-staging-area",
    name="No references outside of its own staging area",
)
def no_references_outside_of_its_own_staging_area(
    manifest: Manifest,
) -> Tuple[List[Node], List[Node]]:
    def staging_depends_on_staging_in_another_area(node: Node):
        different_staging_area_refs = [
            p
            for p in manifest.graph.predecessors(node.id)
            if manifest.get_node(p).is_staging
            if not manifest.get_node(p).area == node.area
        ]
        return node.is_staging and len(list(different_staging_area_refs)) > 0

    passes, failures = partition(
        staging_depends_on_staging_in_another_area, manifest.nodes()
    )
    return list(passes), list(failures)
